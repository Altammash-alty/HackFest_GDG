"""
Configuration file for MedMitra
In a real application, this would load from a config file or database
"""
from medication import Medication, TimeSlot


def load_medications_from_config() -> list[dict]:
    """
    Load medications from configuration
    Returns list of medication dictionaries
    """
    # Example configuration - in real app, this would come from JSON/YAML file or database
    medications_config = [
        {
            "name": "Metoprolol",
            "dosage": "25 mg",
            "time_slot": "Morning",
            "doctor_instructions": "Khane ke baad lein",
            "user_name": "Mr. Sharma"
        },
        {
            "name": "Metformin",
            "dosage": "500 mg",
            "time_slot": "Evening",
            "doctor_instructions": "Khane ke saath lein",
            "user_name": "Mr. Sharma"
        }
    ]
    return medications_config


def create_medication_from_config(config: dict) -> Medication:
    """Create Medication object from configuration dictionary"""
    time_slot_map = {
        "Morning": TimeSlot.MORNING,
        "Afternoon": TimeSlot.AFTERNOON,
        "Evening": TimeSlot.EVENING,
        "Night": TimeSlot.NIGHT
    }
    
    return Medication(
        name=config["name"],
        dosage=config["dosage"],
        time_slot=time_slot_map.get(config["time_slot"], TimeSlot.MORNING),
        doctor_instructions=config.get("doctor_instructions", ""),
        user_name=config.get("user_name", "User")
    )

