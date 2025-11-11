"""
MedMitra - Voice-first medication reminder assistant
Main application entry point
"""
import sys
from datetime import datetime
from .medication import Medication, MedicationManager, TimeSlot
from .voice_handler import VoiceHandler
from .reminder_scheduler import ReminderScheduler
from .caregiver_notifier import CaregiverNotifier


class MedMitra:
    """Main MedMitra application class"""
    
    def __init__(self):
        self.medication_manager = MedicationManager()
        self.voice_handler = VoiceHandler(self.medication_manager)
        self.caregiver_notifier = CaregiverNotifier(self.medication_manager)
        self.scheduler: ReminderScheduler = None
        self.current_medication: Medication = None
    
    def setup_medications(self):
        """Setup sample medications (in real app, load from config/database)"""
        # Example medications - in real app, these would come from user input or database
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
        
        self.medication_manager.add_medication(med1)
        self.medication_manager.add_medication(med2)
        self.medication_manager.user_name = "Mr. Sharma"
        self.medication_manager.set_caregiver_contact("+91-9876543210")
    
    def on_reminder_due(self, medication: Medication):
        """Callback when a medication reminder is due"""
        self.current_medication = medication
        reminder_message = self.voice_handler.generate_reminder(medication)
        
        print("\n" + "="*60)
        print("🔔 MEDICATION REMINDER")
        print("="*60)
        print(reminder_message)
        print("="*60 + "\n")
        
        # In a real voice app, this would use TTS to speak the message
        # For now, we'll just print it
    
    def handle_user_response(self, user_input: str):
        """Handle user's voice/text response"""
        response, medication = self.voice_handler.process_user_input(
            user_input, 
            self.current_medication
        )
        
        if medication and medication != self.current_medication:
            self.current_medication = medication
        
        print("\n" + "-"*60)
        print("MedMitra:", response)
        print("-"*60 + "\n")
        
        # Check if medication was taken and notify caregiver if needed
        if medication and "note kar deta hoon" in response.lower():
            # Medication was taken
            self.scheduler.mark_medication_taken(medication)
            self.current_medication = None
        
        # Check for missed doses and notify caregiver
        if medication:
            notification = self.caregiver_notifier.check_and_notify(medication)
            if notification:
                print(f"\n[Caregiver Alert]: {notification}\n")
    
    def start(self):
        """Start the MedMitra application"""
        print("\n" + "="*60)
        print("  🏥 MedMitra - Medication Reminder Assistant")
        print("="*60)
        print("\nNamaste! Main MedMitra hoon, aapki medication reminder assistant.")
        print("Main aapko sahi waqt par dava lene ki yaad dilaunga.\n")
        
        # Setup medications
        self.setup_medications()
        
        # Start scheduler
        self.scheduler = ReminderScheduler(
            self.medication_manager,
            self.on_reminder_due,
            check_interval=60  # Check every minute
        )
        self.scheduler.start()
        
        print("MedMitra is now active and monitoring your medication schedule.")
        print("Type 'quit' or 'exit' to stop.\n")
        
        # Main interaction loop
        try:
            while True:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop', 'bandh']:
                    print("\nDhanyavaad! MedMitra bandh ho raha hai. Apna dhyan rakhiye!\n")
                    break
                
                if user_input:
                    self.handle_user_response(user_input)
        
        except KeyboardInterrupt:
            print("\n\nDhanyavaad! MedMitra bandh ho raha hai. Apna dhyan rakhiye!\n")
        finally:
            if self.scheduler:
                self.scheduler.stop()


def main():
    """Main entry point"""
    app = MedMitra()
    app.start()


if __name__ == "__main__":
    main()

