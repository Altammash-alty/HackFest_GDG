"""
Voice interaction handler for MedMitra
Handles user responses and generates appropriate Hindi/English mixed responses
"""
from datetime import datetime
from typing import Optional
from .medication import Medication, MedicationManager, TimeSlot


class VoiceHandler:
    """Handles voice/text interactions with the user"""
    
    def __init__(self, medication_manager: MedicationManager):
        self.medication_manager = medication_manager
    
    def get_time_slot_greeting(self, time_slot: TimeSlot) -> str:
        """Get greeting based on time slot"""
        greetings = {
            TimeSlot.MORNING: "subah",
            TimeSlot.AFTERNOON: "dopahar",
            TimeSlot.EVENING: "shaam",
            TimeSlot.NIGHT: "raat"
        }
        return greetings.get(time_slot, "waqt")
    
    def generate_reminder(self, medication: Medication) -> str:
        """Generate a reminder message for medication"""
        user_name = self.medication_manager.user_name
        time_slot_name = self.get_time_slot_greeting(medication.time_slot)
        
        # Build the reminder message
        message = f"Namaste, {user_name}. Ab {time_slot_name} ki dava ka waqt ho gaya hai.\n\n"
        message += f"Dava ka naam hai {medication.name} {medication.dosage}.\n\n"
        
        # Add simple explanation
        explanation = medication.get_simple_explanation()
        message += f"{explanation}\n\n"
        
        # Add doctor instructions if available
        if medication.doctor_instructions:
            message += f"Doctor ki instructions: {medication.doctor_instructions}\n\n"
        
        # Add water reminder
        message += "Kripya ek gilas paani ke saath le lijiye.\n\n"
        message += "Kya aapne dava le li? Aap 'Haan' ya 'Nahi' bol sakte hain."
        
        return message
    
    def handle_yes_response(self, medication: Medication) -> str:
        """Handle when user confirms they took the medication"""
        # Mark as taken
        self.medication_manager.mark_taken(medication, datetime.now())
        
        return ("Bahut accha. Main aapke record mein note kar deta hoon. "
                "Dhanyavaad, apna dhyan rakhiye.")
    
    def handle_no_response(self, medication: Medication) -> str:
        """Handle when user says they haven't taken the medication"""
        return ("Koi baat nahi. Main 10 minute baad dubara yaad kara dunga. "
                "Kripya dava le lijiye.")
    
    def handle_medication_question(self, medication: Medication) -> str:
        """Handle when user asks what the medication is for"""
        explanation = medication.get_simple_explanation()
        return f"{medication.name} {medication.dosage} - {explanation}"
    
    def handle_confused_response(self) -> str:
        """Handle when user seems confused or sad"""
        return ("Main yahan hoon aapki madad ke liye. Aap akelay nahi hain. "
                "Kya main aapki koi aur madad kar sakta hoon?")
    
    def handle_emergency_symptoms(self) -> str:
        """Handle when user mentions severe symptoms"""
        return ("Kripya apne doctor ya nearest clinic se turant sampark karein. "
                "Main emergency medical advice nahi de sakta. "
                "Agar zarurat ho to 102 ya 108 par call karein.")
    
    def process_user_input(self, user_input: str, current_medication: Optional[Medication] = None) -> tuple[str, Optional[Medication]]:
        """
        Process user input and return appropriate response
        Returns: (response_message, medication_if_relevant)
        """
        user_input_lower = user_input.lower().strip()
        
        # Emergency keywords
        emergency_keywords = ["emergency", "severe", "gambhir", "tez dard", "sans nahi aa rahi", 
                             "chest pain", "heart attack", "stroke"]
        if any(keyword in user_input_lower for keyword in emergency_keywords):
            return (self.handle_emergency_symptoms(), None)
        
        # Yes responses
        yes_keywords = ["haan", "yes", "hmm", "le li", "le liya", "ho gaya", "done", "ok"]
        if any(keyword in user_input_lower for keyword in yes_keywords):
            if current_medication:
                return (self.handle_yes_response(current_medication), current_medication)
            return ("Accha. Kya main aapki koi aur madad kar sakta hoon?", None)
        
        # No responses
        no_keywords = ["nahi", "no", "abhi nahi", "baad mein", "not yet", "wait"]
        if any(keyword in user_input_lower for keyword in no_keywords):
            if current_medication:
                return (self.handle_no_response(current_medication), current_medication)
            return ("Theek hai. Kya main aapki koi aur madad kar sakta hoon?", None)
        
        # Medication question
        question_keywords = ["kisliye", "kyun", "kya hai", "what is", "why", "purpose", "kaam"]
        if any(keyword in user_input_lower for keyword in question_keywords):
            if current_medication:
                return (self.handle_medication_question(current_medication), current_medication)
            # Try to find medication in input
            for med in self.medication_manager.medications:
                if med.name.lower() in user_input_lower:
                    return (self.handle_medication_question(med), med)
            return ("Kya aap kisi specific dava ke baare mein poochh rahe hain? "
                   "Kripya dava ka naam bataiye.", None)
        
        # Confused/sad responses
        confused_keywords = ["confused", "sad", "upset", "pareshan", "udaas", "samajh nahi aa raha"]
        if any(keyword in user_input_lower for keyword in confused_keywords):
            return (self.handle_confused_response(), None)
        
        # Default response
        return ("Main aapki baat samajh nahi paya. Kya aap 'Haan' ya 'Nahi' bol sakte hain? "
               "Ya phir aap koi sawaal poochh sakte hain.", current_medication)

