# MedMitra Quick Start Guide

## Getting Started

### 1. Run the Demo

To see MedMitra in action without waiting for actual medication times:

```bash
python run_demo.py
```

This demonstrates:
- Medication reminders
- User confirmation (Yes/No)
- Medication explanations
- Emergency handling
- Emotional support
- Caregiver notifications

### 2. Run the Full Application

To start MedMitra with time-based reminders:

```bash
python run_medmitra.py
```

Or:

```bash
python -m medmitra.main
```

The application will:
- Load medication schedules
- Monitor the current time
- Display reminders when medication time arrives
- Wait for your input (Haan/Nahi)
- Track medication intake

### 3. Example Interaction

```
🔔 MEDICATION REMINDER
============================================================
Namaste, Mr. Sharma. Ab subah ki dava ka waqt ho gaya hai.

Dava ka naam hai Metoprolol 25 mg.

Yeh dawa aapke blood pressure aur dil ki dhadkan ko normal rakhti hai...

Kya aapne dava le li? Aap 'Haan' ya 'Nahi' bol sakte hain.
============================================================

You: Haan

MedMitra: Bahut accha. Main aapke record mein note kar deta hoon. 
          Dhanyavaad, apna dhyan rakhiye.
```

## Customizing Medications

Edit `medmitra/main.py` in the `setup_medications()` method:

```python
medication = Medication(
    name="Your Medication Name",
    dosage="Dosage amount",
    time_slot=TimeSlot.MORNING,  # or AFTERNOON, EVENING, NIGHT
    doctor_instructions="Instructions here",
    user_name="User Name"
)
```

## Available Commands

When interacting with MedMitra, you can say:

- **"Haan"** or **"Yes"** - Confirm medication taken
- **"Nahi"** or **"No"** - Haven't taken yet
- **"Yeh dawa kisliye hai?"** - Ask what the medicine is for
- **"quit"** or **"exit"** - Stop the application

## Key Features

✅ Automatic time-based reminders  
✅ Simple Hindi/English explanations  
✅ User-friendly confirmation system  
✅ Caregiver notifications for missed doses  
✅ Emergency situation handling  
✅ Compassionate, respectful tone  

## Next Steps

For production use, consider:
- Adding voice input/output (speech recognition + TTS)
- Database storage for medication history
- SMS/WhatsApp integration for caregiver alerts
- Mobile app interface
- Multi-user support

---

**Note**: MedMitra is a reminder assistant, not a replacement for medical care. Always consult healthcare professionals for medical advice.

