"""
MedMitra Web Application - Flask-based voice assistant
Provides REST API and WebSocket support for voice interactions
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime
import json
import os

from .medication import Medication, MedicationManager, TimeSlot
from .voice_handler import VoiceHandler
from .reminder_scheduler import ReminderScheduler
from .caregiver_notifier import CaregiverNotifier

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global instances
medication_manager = MedicationManager()
voice_handler = VoiceHandler(medication_manager)
caregiver_notifier = CaregiverNotifier(medication_manager)
scheduler = None
current_medication = None


@app.route('/')
def index():
    """Serve the main application page (Patient App)"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Serve the caregiver dashboard"""
    return render_template('dashboard.html')


@app.route('/static/sw.js')
def service_worker():
    """Serve service worker"""
    return app.send_static_file('sw.js'), 200, {'Content-Type': 'application/javascript'}


@app.route('/api/medications', methods=['GET'])
def get_medications():
    """Get list of all medications"""
    medications = []
    for med in medication_manager.medications:
        medications.append({
            'name': med.name,
            'dosage': med.dosage,
            'time_slot': med.time_slot.value,
            'doctor_instructions': med.doctor_instructions,
            'user_name': med.user_name
        })
    return jsonify({'medications': medications})


@app.route('/api/medications', methods=['POST'])
def add_medication():
    """Add a new medication"""
    data = request.json
    try:
        time_slot_map = {
            'Morning': TimeSlot.MORNING,
            'Afternoon': TimeSlot.AFTERNOON,
            'Evening': TimeSlot.EVENING,
            'Night': TimeSlot.NIGHT
        }
        
        medication = Medication(
            name=data['name'],
            dosage=data['dosage'],
            time_slot=time_slot_map.get(data['time_slot'], TimeSlot.MORNING),
            doctor_instructions=data.get('doctor_instructions', ''),
            user_name=data.get('user_name', 'User')
        )
        
        medication_manager.add_medication(medication)
        
        # Notify connected clients
        socketio.emit('medication_added', {
            'medication': {
                'name': medication.name,
                'dosage': medication.dosage,
                'time_slot': medication.time_slot.value
            }
        })
        
        return jsonify({'success': True, 'message': 'Medication added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/medications/<medication_name>', methods=['DELETE'])
def delete_medication(medication_name):
    """Delete a medication"""
    try:
        # Find and remove medication
        medication_to_remove = None
        for med in medication_manager.medications:
            if med.name == medication_name:
                medication_to_remove = med
                break
        
        if medication_to_remove:
            medication_manager.medications.remove(medication_to_remove)
            
            # Notify connected clients
            socketio.emit('medication_deleted', {
                'medication_name': medication_name
            })
            
            return jsonify({'success': True, 'message': 'Medication deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Medication not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get medication history"""
    try:
        history = []
        for record in medication_manager.records:
            history.append({
                'medication_name': record.medication.name,
                'dosage': record.medication.dosage,
                'scheduled_time': record.scheduled_time.isoformat(),
                'taken': record.taken,
                'taken_time': record.taken_time.isoformat() if record.taken_time else None,
                'missed': record.missed,
                'reminder_count': record.reminder_count
            })
        
        # Sort by scheduled time, most recent first
        history.sort(key=lambda x: x['scheduled_time'], reverse=True)
        
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/user/response', methods=['POST'])
def handle_user_response():
    """Handle user voice/text response"""
    global current_medication
    
    data = request.json
    user_input = data.get('text', '').strip()
    
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    
    # Process user input
    response, medication = voice_handler.process_user_input(user_input, current_medication)
    
    if medication and medication != current_medication:
        current_medication = medication
    
    # Mark as taken if confirmed
    medication_taken = False
    if medication:
        user_input_lower = user_input.lower()
        # Check for yes responses
        yes_keywords = ["haan", "yes", "hmm", "le li", "le liya", "ho gaya", "done", "ok"]
        if any(keyword in user_input_lower for keyword in yes_keywords) or "note kar deta hoon" in response.lower():
            if scheduler:
                scheduler.mark_medication_taken(medication)
            medication_manager.mark_taken(medication, datetime.now())
            current_medication = None
            medication_taken = True
            
            # Notify caregiver dashboard
            socketio.emit('medication_taken', {
                'medication': {
                    'name': medication.name,
                    'dosage': medication.dosage
                },
                'timestamp': datetime.now().isoformat()
            })
    
    # Check for caregiver notifications
    caregiver_alert = None
    if medication:
        caregiver_alert = caregiver_notifier.check_and_notify(medication)
    
    return jsonify({
        'response': response,
        'caregiver_alert': caregiver_alert,
        'medication_taken': medication_taken
    })


@app.route('/api/reminder/current', methods=['GET'])
def get_current_reminder():
    """Get current active reminder if any"""
    global current_medication
    
    if current_medication:
        reminder_text = voice_handler.generate_reminder(current_medication)
        return jsonify({
            'has_reminder': True,
            'medication': {
                'name': current_medication.name,
                'dosage': current_medication.dosage,
                'time_slot': current_medication.time_slot.value
            },
            'reminder_text': reminder_text
        })
    
    return jsonify({'has_reminder': False})


@app.route('/api/setup', methods=['POST'])
def setup_user():
    """Setup user information and caregiver contact"""
    data = request.json
    medication_manager.user_name = data.get('user_name', 'User')
    medication_manager.set_caregiver_contact(data.get('caregiver_contact', ''))
    
    return jsonify({'success': True, 'message': 'User setup completed'})


def on_reminder_due(medication):
    """Callback when a medication reminder is due"""
    global current_medication
    current_medication = medication
    reminder_message = voice_handler.generate_reminder(medication)
    
    # Emit reminder to all connected clients
    socketio.emit('medication_reminder', {
        'medication': {
            'name': medication.name,
            'dosage': medication.dosage,
            'time_slot': medication.time_slot.value,
            'doctor_instructions': medication.doctor_instructions
        },
        'message': reminder_message,
        'timestamp': datetime.now().isoformat()
    })


def initialize_scheduler():
    """Initialize the reminder scheduler"""
    global scheduler
    if scheduler is None:
        scheduler = ReminderScheduler(
            medication_manager,
            on_reminder_due,
            check_interval=60
        )
        scheduler.start()
    return scheduler


# Initialize with sample medications
def setup_sample_medications():
    """Setup sample medications for demo"""
    if len(medication_manager.medications) == 0:
        med1 = Medication(
            name="Metoprolol",
            dosage="25 mg",
            time_slot=TimeSlot.MORNING,
            doctor_instructions="Khane ke baad lein",
            user_name="Mr. Sharma"
        )
        
        med2 = Medication(
            name="Metformin",
            dosage="500 mg",
            time_slot=TimeSlot.EVENING,
            doctor_instructions="Khane ke saath lein",
            user_name="Mr. Sharma"
        )
        
        medication_manager.add_medication(med1)
        medication_manager.add_medication(med2)
        medication_manager.user_name = "Mr. Sharma"
        medication_manager.set_caregiver_contact("+91-9876543210")


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connected', {'message': 'Connected to MedMitra'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


@socketio.on('ping')
def handle_ping():
    """Handle ping to keep connection alive"""
    emit('pong', {'status': 'ok'})


@socketio.on('user_message')
def handle_user_message(data):
    """Handle user message via WebSocket"""
    global current_medication
    
    user_input = data.get('text', '').strip()
    if not user_input:
        return
    
    # Process user input
    response, medication = voice_handler.process_user_input(user_input, current_medication)
    
    if medication and medication != current_medication:
        current_medication = medication
    
    # Check if medication was taken (multiple ways to confirm)
    medication_taken = False
    user_input_lower = user_input.lower()
    response_lower = response.lower()
    
    # Check various ways user might confirm
    if (any(word in user_input_lower for word in ['haan', 'yes', 'le li', 'le liya', 'ho gaya', 'done', 'ok', 'hmm']) or
        "note kar deta hoon" in response_lower):
        medication_taken = True
        if medication:
            if scheduler:
                scheduler.mark_medication_taken(medication)
            medication_manager.mark_taken(medication, datetime.now())
            current_medication = None
            
            # Notify caregiver dashboard
            emit('medication_taken', {
                'medication': {
                    'name': medication.name,
                    'dosage': medication.dosage
                },
                'timestamp': datetime.now().isoformat()
            })
    
    # Check for caregiver notifications
    caregiver_alert = None
    if medication:
        caregiver_alert = caregiver_notifier.check_and_notify(medication)
    
    # Emit response back to client
    emit('medmitra_response', {
        'response': response,
        'caregiver_alert': caregiver_alert,
        'medication_taken': medication_taken,
        'medication': {
            'name': medication.name if medication else None,
            'dosage': medication.dosage if medication else None
        } if medication else None
    })


if __name__ == '__main__':
    setup_sample_medications()
    initialize_scheduler()
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*60)
    print("  🏥 MedMitra Web Server Starting...")
    print("="*60)
    print(f"Server running on: http://localhost:{port}")
    print(f"Access from mobile: http://<your-ip>:{port}")
    print("="*60 + "\n")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug, allow_unsafe_werkzeug=True)

