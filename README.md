# MedMitra - Voice-First Medication Reminder Assistant

MedMitra is a compassionate, voice-first medication reminder assistant designed specifically for elderly users who may have difficulty reading, remembering schedules, or operating complex apps.

## Features

### Core Capabilities

1. **Time-based Medication Reminders**
   - Automatic reminders at scheduled times (Morning, Afternoon, Evening, Night)
   - Configurable medication schedules
   - Multiple medication support

2. **Simple Medication Explanations**
   - Explains medications in simple Hindi/English mix
   - Uses everyday analogies instead of medical jargon
   - Answers "Yeh dawa kisliye hai?" (What is this medicine for?)

3. **User Confirmation System**
   - Confirms whether medication has been taken
   - Tracks medication intake history
   - Handles "Haan" (Yes) and "Nahi" (No) responses

4. **Caregiver Notifications**
   - Alerts caregivers when doses are missed repeatedly
   - Non-threatening, supportive messaging
   - Tracks missed dose patterns

5. **Compassionate Interaction**
   - Warm, polite, human-like tone
   - Patient and encouraging responses
   - Never scolds or guilt-trips users
   - Handles confusion and emotional support

## Installation

1. Clone or download this repository
2. Install Python 3.7 or higher
3. Install dependencies (if needed for voice features):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🌐 Web Application (Recommended for Mobile/Desktop)

**Start the web server:**
```bash
pip install -r requirements.txt
python run_web.py
```

Then open `http://localhost:5000` in your browser, or access from mobile device using your computer's IP address.

**📱 Mobile Access:** See [MOBILE_ACCESS.md](MOBILE_ACCESS.md) for step-by-step instructions.

**Features:**
- 🎤 Voice input/output (Web Speech API)
- 📱 Mobile-responsive design
- 🔔 Real-time medication reminders
- 📲 Installable as PWA app
- 🌐 Works on any device with a browser

See [WEB_SETUP.md](WEB_SETUP.md) for detailed setup instructions.

### 💻 Terminal Application

**Option 1: Use the launcher script**
```bash
python run_medmitra.py
```

**Option 2: Run as a module**
```bash
python -m medmitra.main
```

**Option 3: Run the demo**
```bash
python run_demo.py
```

### How It Works

1. **Setup**: The application loads medication schedules (currently from code, but can be configured)
2. **Monitoring**: The scheduler continuously monitors the current time
3. **Reminders**: When medication time arrives, MedMitra displays a reminder message
4. **Interaction**: User responds with "Haan" (Yes) or "Nahi" (No)
5. **Tracking**: System tracks intake and notifies caregivers if needed

### Example Interaction

```
🔔 MEDICATION REMINDER
============================================================
Namaste, Mr. Sharma. Ab subah ki dava ka waqt ho gaya hai.

Dava ka naam hai Metoprolol 25 mg.

Yeh dawa aapke blood pressure aur dil ki dhadkan ko normal rakhti hai, taaki dil ko zyada mehnat na karni pade.

Doctor ki instructions: Khane ke baad lein

Kripya ek gilas paani ke saath le lijiye.

Kya aapne dava le li? Aap 'Haan' ya 'Nahi' bol sakte hain.
============================================================

You: Haan

------------------------------------------------------------
MedMitra: Bahut accha. Main aapke record mein note kar deta hoon. Dhanyavaad, apna dhyan rakhiye.
------------------------------------------------------------
```

## Project Structure

```
medmitra/
├── __init__.py              # Package initialization
├── main.py                  # Main application entry point
├── medication.py            # Medication data structures and management
├── voice_handler.py         # Voice/text interaction handling
├── reminder_scheduler.py    # Time-based reminder scheduling
├── caregiver_notifier.py    # Caregiver notification system
└── config.py                # Configuration management
```

## Configuration

### Adding Medications

Edit `medmitra/main.py` or use the config system to add medications:

```python
medication = Medication(
    name="Metoprolol",
    dosage="25 mg",
    time_slot=TimeSlot.MORNING,
    doctor_instructions="Khane ke baad lein",
    user_name="Mr. Sharma"
)
```

### Time Slots

- `TimeSlot.MORNING` - 8:00 AM
- `TimeSlot.AFTERNOON` - 2:00 PM
- `TimeSlot.EVENING` - 6:00 PM
- `TimeSlot.NIGHT` - 9:00 PM

## Key Design Principles

1. **Compassion First**: Never scold, shame, or threaten users
2. **Simplicity**: Use simple words, avoid medical jargon
3. **Clarity**: Speak slowly and clearly (in voice implementation)
4. **Safety**: Never prescribe or give emergency medical advice
5. **Respect**: Treat users like respected elders in the family

## Safety Features

- **No Prescription**: MedMitra never prescribes new medicines
- **No Emergency Advice**: Directs users to contact doctors/clinics for emergencies
- **Emergency Detection**: Recognizes emergency keywords and responds appropriately

## Future Enhancements

- Voice input/output integration (speech recognition + TTS)
- SMS/WhatsApp notifications for caregivers
- Database storage for medication history
- Mobile app interface
- Multi-language support
- Integration with pharmacy systems

## License

This project is designed for healthcare assistance. Please ensure compliance with healthcare data regulations (HIPAA, etc.) when deploying.

## Support

For questions or issues, please refer to the code documentation or create an issue in the repository.

---

**Remember**: MedMitra is a reminder assistant, not a replacement for medical care. Always consult healthcare professionals for medical advice.

