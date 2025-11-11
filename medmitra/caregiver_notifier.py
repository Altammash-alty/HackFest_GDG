"""
Caregiver notification system for MedMitra
Sends alerts when doses are missed repeatedly
"""
from datetime import datetime
from typing import Optional
from .medication import Medication, MedicationManager


class CaregiverNotifier:
    """Handles notifications to caregivers"""
    
    def __init__(self, medication_manager: MedicationManager):
        self.medication_manager = medication_manager
        self.notification_history: list[dict] = []
    
    def check_and_notify(self, medication: Medication):
        """
        Check if medication has been missed repeatedly and notify caregiver
        Returns notification message if sent, None otherwise
        """
        missed_count = self.medication_manager.get_missed_count(medication, days=1)
        
        # Notify if 2 or more doses missed in a day
        if missed_count >= 2:
            return self.send_notification(medication, missed_count)
        
        return None
    
    def send_notification(self, medication: Medication, missed_count: int) -> str:
        """
        Send notification to caregiver
        Returns the notification message
        """
        user_name = self.medication_manager.user_name
        time_slot = medication.time_slot.value
        
        message = (f"{user_name} ne aaj {time_slot} ki dava miss ki hai. "
                  f"Total {missed_count} doses miss ho chuki hain. "
                  f"Kripya unse baat karein aur unki madad karein.")
        
        # Store notification in history
        notification = {
            "timestamp": datetime.now(),
            "user": user_name,
            "medication": medication.name,
            "missed_count": missed_count,
            "message": message
        }
        self.notification_history.append(notification)
        
        # In a real implementation, this would send SMS/email/WhatsApp
        # For now, we'll just log it
        self._log_notification(notification)
        
        return message
    
    def _log_notification(self, notification: dict):
        """Log notification (in real app, this would send via SMS/email/WhatsApp)"""
        timestamp = notification["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[CAREGIVER NOTIFICATION - {timestamp}]")
        print(f"To: {self.medication_manager.caregiver_contact}")
        print(f"Message: {notification['message']}\n")
    
    def get_notification_history(self) -> list[dict]:
        """Get history of all notifications sent"""
        return self.notification_history

