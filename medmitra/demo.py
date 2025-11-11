"""
Demo script to showcase MedMitra functionality
This demonstrates the interaction flow without waiting for actual time-based reminders
"""
import sys
import os
# Add parent directory to path for standalone script execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from medmitra.medication import Medication, MedicationManager, TimeSlot
from medmitra.voice_handler import VoiceHandler
from medmitra.caregiver_notifier import CaregiverNotifier
from datetime import datetime


def demo_medmitra():
    """Demonstrate MedMitra's key features"""
    
    print("\n" + "="*70)
    print("  🏥 MedMitra - Medication Reminder Assistant - DEMO")
    print("="*70 + "\n")
    
    # Setup
    manager = MedicationManager()
    manager.user_name = "Mr. Sharma"
    manager.set_caregiver_contact("+91-9876543210")
    
    voice_handler = VoiceHandler(manager)
    caregiver_notifier = CaregiverNotifier(manager)
    
    # Add sample medications
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
    
    manager.add_medication(med1)
    manager.add_medication(med2)
    
    print("📋 Sample Medications Added:")
    print(f"  1. {med1.name} {med1.dosage} - {med1.time_slot.value}")
    print(f"  2. {med2.name} {med2.dosage} - {med2.time_slot.value}\n")
    
    # Demo 1: Generate Reminder
    print("="*70)
    print("DEMO 1: Medication Reminder")
    print("="*70)
    reminder = voice_handler.generate_reminder(med1)
    print(reminder)
    print()
    
    # Demo 2: User says "Haan" (Yes)
    print("="*70)
    print("DEMO 2: User Confirms Medication Taken")
    print("="*70)
    print("User: Haan")
    response, _ = voice_handler.process_user_input("Haan", med1)
    print(f"MedMitra: {response}\n")
    
    # Demo 3: User asks about medication
    print("="*70)
    print("DEMO 3: User Asks About Medication")
    print("="*70)
    print("User: Yeh dawa kisliye hai?")
    response, _ = voice_handler.process_user_input("Yeh dawa kisliye hai?", med1)
    print(f"MedMitra: {response}\n")
    
    # Demo 4: User says "Nahi" (No)
    print("="*70)
    print("DEMO 4: User Hasn't Taken Medication Yet")
    print("="*70)
    print("User: Nahi")
    response, _ = voice_handler.process_user_input("Nahi", med2)
    print(f"MedMitra: {response}\n")
    
    # Demo 5: Emergency Response
    print("="*70)
    print("DEMO 5: Emergency Situation Handling")
    print("="*70)
    print("User: Mujhe tez dard ho raha hai")
    response, _ = voice_handler.process_user_input("Mujhe tez dard ho raha hai")
    print(f"MedMitra: {response}\n")
    
    # Demo 6: Confused User Support
    print("="*70)
    print("DEMO 6: Emotional Support")
    print("="*70)
    print("User: Main pareshan hoon")
    response, _ = voice_handler.process_user_input("Main pareshan hoon")
    print(f"MedMitra: {response}\n")
    
    # Demo 7: Caregiver Notification
    print("="*70)
    print("DEMO 7: Caregiver Notification (After Multiple Missed Doses)")
    print("="*70)
    
    # Simulate missed doses
    from medmitra.medication import MedicationRecord
    record1 = MedicationRecord(med1, datetime.now(), missed=True)
    record2 = MedicationRecord(med1, datetime.now(), missed=True)
    manager.records.extend([record1, record2])
    
    notification = caregiver_notifier.check_and_notify(med1)
    if notification:
        print(f"Notification: {notification}\n")
    
    print("="*70)
    print("Demo Complete! MedMitra is ready to help.")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo_medmitra()

