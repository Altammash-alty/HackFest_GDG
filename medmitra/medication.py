"""
Medication data structure and management for MedMitra
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, time
from enum import Enum


class TimeSlot(Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    NIGHT = "Night"


@dataclass
class Medication:
    """Represents a medication with all necessary information"""
    name: str
    dosage: str
    time_slot: TimeSlot
    doctor_instructions: str
    user_name: str = "User"
    
    def get_time(self) -> time:
        """Get the time for this medication based on time slot"""
        time_map = {
            TimeSlot.MORNING: time(8, 0),      # 8:00 AM
            TimeSlot.AFTERNOON: time(14, 0),   # 2:00 PM
            TimeSlot.EVENING: time(18, 0),     # 6:00 PM
            TimeSlot.NIGHT: time(21, 0)        # 9:00 PM
        }
        return time_map[self.time_slot]
    
    def get_simple_explanation(self) -> str:
        """Get a simple explanation of what this medication does"""
        explanations = {
            "metformin": "Yeh dawa aapke blood sugar ko control karti hai, taaki aap healthy rahein.",
            "metoprolol": "Yeh dawa aapke blood pressure aur dil ki dhadkan ko normal rakhti hai, taaki dil ko zyada mehnat na karni pade.",
            "aspirin": "Yeh dawa blood ko thin rakhti hai, taaki clots na banein aur heart healthy rahe.",
            "atorvastatin": "Yeh dawa cholesterol ko kam karti hai, taaki heart aur blood vessels sahi kaam karein.",
            "amlodipine": "Yeh dawa blood pressure ko kam karti hai, taaki dil aur blood vessels par zyada pressure na pade.",
            "omeprazole": "Yeh dawa pet ki acid ko kam karti hai, taaki pet mein jalan na ho.",
            "levothyroxine": "Yeh dawa thyroid gland ko sahi kaam karne mein madad karti hai.",
        }
        
        name_lower = self.name.lower()
        for key, explanation in explanations.items():
            if key in name_lower:
                return explanation
        
        # Generic explanation if specific one not found
        return f"Yeh dawa aapke doctor ne aapki sehat ke liye prescribe ki hai. Kripya doctor ke instructions ke mutabik lein."


@dataclass
class MedicationRecord:
    """Tracks medication intake history"""
    medication: Medication
    scheduled_time: datetime
    taken: bool = False
    taken_time: Optional[datetime] = None
    reminder_count: int = 0
    missed: bool = False


class MedicationManager:
    """Manages medications and their schedules"""
    
    def __init__(self):
        self.medications: List[Medication] = []
        self.records: List[MedicationRecord] = []
        self.caregiver_contact: Optional[str] = None
        self.user_name: str = "User"
    
    def add_medication(self, medication: Medication):
        """Add a new medication to the schedule"""
        self.medications.append(medication)
        if not self.user_name or self.user_name == "User":
            self.user_name = medication.user_name
    
    def get_medications_for_time(self, current_time: datetime) -> List[Medication]:
        """Get medications due at the current time"""
        due_medications = []
        current_time_only = current_time.time()
        
        for med in self.medications:
            med_time = med.get_time()
            # Check if current time matches scheduled time (within 5 minutes)
            # This ensures reminders trigger exactly at the right time
            time_diff = abs((current_time_only.hour * 60 + current_time_only.minute) - 
                          (med_time.hour * 60 + med_time.minute))
            if time_diff <= 5:
                due_medications.append(med)
        
        return due_medications
    
    def create_record(self, medication: Medication, scheduled_time: datetime) -> MedicationRecord:
        """Create a new medication record"""
        record = MedicationRecord(medication=medication, scheduled_time=scheduled_time)
        self.records.append(record)
        return record
    
    def mark_taken(self, medication: Medication, taken_time: datetime):
        """Mark medication as taken"""
        # Find the most recent record for this medication
        for record in reversed(self.records):
            if record.medication.name == medication.name and not record.taken:
                record.taken = True
                record.taken_time = taken_time
                record.missed = False
                return record
        return None
    
    def get_missed_count(self, medication: Medication, days: int = 1) -> int:
        """Get count of missed doses for a medication in recent days"""
        cutoff = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        missed_count = 0
        
        for record in self.records:
            if (record.medication.name == medication.name and 
                record.scheduled_time >= cutoff and 
                record.missed):
                missed_count += 1
        
        return missed_count
    
    def set_caregiver_contact(self, contact: str):
        """Set caregiver contact information"""
        self.caregiver_contact = contact

