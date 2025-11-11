# Automatic Medication Reminders - How It Works

## Overview

MedMitra automatically runs in the background and triggers medication reminders at the exact prescribed times. Users can respond with voice commands to confirm whether they took their medication.

## How Automatic Reminders Work

### 1. **Background Scheduler**
- The scheduler runs continuously, checking every 30 seconds for due medications
- When a medication time arrives (within 5 minutes of scheduled time), it automatically triggers a reminder
- No user interaction needed - reminders appear automatically

### 2. **Reminder Display**
- Reminders appear prominently with:
  - 🔔 Pulsing red card at the top
  - Spoken aloud using text-to-speech
  - Clear medication information
  - Instructions to respond

### 3. **Auto Voice Listening**
- After the reminder is spoken, voice listening automatically starts
- User can simply say "Haan" (Yes) or "Nahi" (No)
- No need to tap buttons - just speak naturally

### 4. **Voice Command Recognition**
The system recognizes multiple ways to confirm:

**"Yes" responses:**
- "Haan" (Hindi)
- "Yes"
- "Le li" / "Le liya" (I took it)
- "Ho gaya" (Done)
- "Ok" / "Done"

**"No" responses:**
- "Nahi" (Hindi)
- "No"
- "Abhi nahi" (Not yet)

### 5. **Automatic Tracking**
- When user says "Haan", medication is automatically recorded as taken
- Reminder card disappears after confirmation
- If user says "Nahi", system will remind again in 10 minutes

## Medication Schedule

Default times (can be customized):
- **Morning**: 8:00 AM
- **Afternoon**: 2:00 PM
- **Evening**: 6:00 PM
- **Night**: 9:00 PM

## Example Flow

1. **8:00 AM** - System automatically detects it's morning medication time
2. **Reminder appears** - Red pulsing card with medication details
3. **MedMitra speaks** - "Namaste, Mr. Sharma. Ab subah ki dava ka waqt ho gaya hai..."
4. **Voice listening starts** - Automatically after 3 seconds
5. **User speaks** - "Haan" (Yes)
6. **System confirms** - "Bahut accha. Main aapke record mein note kar deta hoon."
7. **Reminder disappears** - Medication recorded successfully

## Features

✅ **Fully Automatic** - No need to check manually  
✅ **Voice-First** - Just speak to confirm  
✅ **Multiple Languages** - Hindi and English  
✅ **Smart Recognition** - Understands various ways to say yes/no  
✅ **Persistent** - Keeps reminding if medication not taken  
✅ **Caregiver Alerts** - Notifies if doses missed repeatedly  

## Testing Automatic Reminders

To test without waiting for actual time:

1. **Modify medication time** in `medmitra/app.py`:
   ```python
   med1 = Medication(
       name="Metoprolol",
       dosage="25 mg",
       time_slot=TimeSlot.MORNING,  # Change this
       ...
   )
   ```

2. **Or temporarily change time slot times** in `medication.py`:
   ```python
   time_map = {
       TimeSlot.MORNING: time(8, 0),  # Change to current time + 1 minute
       ...
   }
   ```

3. **Start the server** and wait for the reminder to trigger automatically

## Requirements

- Web browser must be open and connected
- Microphone permissions granted
- Server must be running continuously
- Device should not be in sleep mode (for accurate timing)

## Troubleshooting

**Reminders not appearing?**
- Check if server is running
- Verify medication times are set correctly
- Check browser console for errors
- Ensure WebSocket connection is active (green status indicator)

**Voice not working?**
- Grant microphone permissions
- Check browser compatibility (Chrome/Safari recommended)
- Use text input as fallback

**Reminders too frequent?**
- Adjust `check_interval` in `reminder_scheduler.py` (default: 30 seconds)
- Adjust time window in `get_medications_for_time()` (default: 5 minutes)

---

The system is designed to work completely automatically - just keep the browser open and MedMitra will handle the rest!

