"""
Reminder scheduling system for MedMitra
Manages time-based medication reminders
"""
import threading
import time as time_module
from datetime import datetime, time
from typing import Callable, Optional
from .medication import Medication, MedicationManager, MedicationRecord, TimeSlot


class ReminderScheduler:
    """Manages scheduled medication reminders"""
    
    def __init__(self, medication_manager: MedicationManager, 
                 reminder_callback: Callable[[Medication], None],
                 check_interval: int = 30):
        """
        Initialize scheduler
        Args:
            medication_manager: Manager for medications
            reminder_callback: Function to call when reminder is due
            check_interval: How often to check for due medications (in seconds)
        """
        self.medication_manager = medication_manager
        self.reminder_callback = reminder_callback
        self.check_interval = check_interval
        self.running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.pending_reminders: dict[str, MedicationRecord] = {}
    
    def start(self):
        """Start the reminder scheduler"""
        if self.running:
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        print("MedMitra reminder scheduler started.")
    
    def stop(self):
        """Stop the reminder scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=2)
        print("MedMitra reminder scheduler stopped.")
    
    def _scheduler_loop(self):
        """Main scheduler loop that checks for due medications"""
        while self.running:
            try:
                current_time = datetime.now()
                due_medications = self.medication_manager.get_medications_for_time(current_time)
                
                for medication in due_medications:
                    # Check if we already have a pending reminder for this medication today
                    reminder_key = f"{medication.name}_{current_time.date()}"
                    
                    if reminder_key not in self.pending_reminders:
                        # Create a record for this reminder
                        scheduled_datetime = current_time.replace(
                            hour=medication.get_time().hour,
                            minute=medication.get_time().minute,
                            second=0,
                            microsecond=0
                        )
                        record = self.medication_manager.create_record(medication, scheduled_datetime)
                        self.pending_reminders[reminder_key] = record
                        
                        # Trigger reminder
                        self.reminder_callback(medication)
                
                # Check for missed medications (not taken after 1 hour of scheduled time)
                self._check_missed_medications(current_time)
                
            except Exception as e:
                print(f"Error in scheduler loop: {e}")
            
            time_module.sleep(self.check_interval)
    
    def _check_missed_medications(self, current_time: datetime):
        """Check if any medications were missed and mark them"""
        for key, record in list(self.pending_reminders.items()):
            if not record.taken:
                # If more than 1 hour has passed since scheduled time
                time_diff = (current_time - record.scheduled_time).total_seconds() / 3600
                if time_diff > 1:
                    record.missed = True
                    record.reminder_count += 1
                    
                    # If reminder count is high, mark as missed
                    if record.reminder_count >= 3:
                        # This will be handled by caregiver notifier
                        pass
    
    def mark_medication_taken(self, medication: Medication):
        """Mark medication as taken and remove from pending reminders"""
        current_date = datetime.now().date()
        reminder_key = f"{medication.name}_{current_date}"
        
        if reminder_key in self.pending_reminders:
            record = self.pending_reminders[reminder_key]
            record.taken = True
            record.taken_time = datetime.now()
            # Don't remove from pending, just mark as taken (for history)
    
    def get_pending_reminders(self) -> list[MedicationRecord]:
        """Get list of pending reminders"""
        return [record for record in self.pending_reminders.values() if not record.taken]

