# MedMitra Web Application Setup Guide

## Overview

MedMitra is now a **full-fledged web-based voice assistant** that works on any device with a web browser (mobile phones, tablets, desktops). It features:

- 🎤 **Voice Input/Output** - Uses Web Speech API for voice interactions
- 📱 **Mobile-First Design** - Responsive UI optimized for mobile devices
- 🔔 **Real-time Reminders** - WebSocket-based real-time medication reminders
- 📲 **PWA Support** - Can be installed as an app on mobile devices
- 🌐 **Cross-Platform** - Works on iOS, Android, Windows, macOS, Linux

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Flask-SocketIO (WebSocket support)
- Eventlet (async server)

### 2. Start the Web Server

```bash
python run_web.py
```

The server will start on `http://localhost:5000`

### 3. Access from Mobile Device

1. **Find your computer's IP address:**
   - Windows: Open Command Prompt and type `ipconfig`
   - Mac/Linux: Open Terminal and type `ifconfig` or `ip addr`
   - Look for IPv4 address (e.g., 192.168.1.100)

2. **On your mobile device:**
   - Make sure your mobile device is on the same Wi-Fi network
   - Open a web browser (Chrome, Safari, etc.)
   - Go to: `http://<your-ip>:5000`
   - Example: `http://192.168.1.100:5000`

3. **Install as PWA (Optional):**
   - On Android: Browser will show "Add to Home Screen" option
   - On iOS: Tap Share button → "Add to Home Screen"
   - The app will work offline after first load!

## Features

### Voice Interaction

- **Tap the microphone button** to speak
- Supports Hindi and English (India)
- Automatically converts speech to text
- MedMitra responds with voice output

### Text Input (Fallback)

- If voice doesn't work, use the text input field
- Type your response and press Send or Enter

### Real-time Reminders

- Medication reminders appear automatically
- Spoken aloud for accessibility
- User can respond with "Haan" (Yes) or "Nahi" (No)

### Mobile-Optimized

- Large touch-friendly buttons
- Responsive design adapts to screen size
- Works in portrait and landscape mode
- Smooth animations and transitions

## Browser Compatibility

### Voice Input (Web Speech API)
- ✅ Chrome/Edge (Android, Desktop)
- ✅ Safari (iOS 14.5+, macOS)
- ⚠️ Firefox (limited support)
- ❌ Older browsers (fallback to text input)

### Voice Output (Text-to-Speech)
- ✅ All modern browsers
- ✅ Supports Hindi and English voices

### PWA Features
- ✅ Android (Chrome, Edge)
- ✅ iOS (Safari 11.3+)
- ✅ Desktop browsers

## Configuration

### Change Port

Set environment variable:
```bash
# Windows PowerShell
$env:PORT=8080
python run_web.py

# Mac/Linux
PORT=8080 python run_web.py
```

### Enable Debug Mode

```bash
# Windows PowerShell
$env:DEBUG="True"
python run_web.py

# Mac/Linux
DEBUG=True python run_web.py
```

## Production Deployment

For production, consider:

1. **Use a production server:**
   ```bash
   pip install gunicorn
   gunicorn -k eventlet -w 1 --bind 0.0.0.0:5000 medmitra.app:app
   ```

2. **Use HTTPS:**
   - Required for Web Speech API on some browsers
   - Use Let's Encrypt for free SSL certificate
   - Or use a reverse proxy (nginx) with SSL

3. **Database Storage:**
   - Currently uses in-memory storage
   - Add SQLite/PostgreSQL for persistent storage

4. **SMS/Email Notifications:**
   - Integrate Twilio for SMS
   - Integrate SendGrid for email

## Troubleshooting

### Voice not working?
- Check browser compatibility
- Ensure microphone permissions are granted
- Try text input as fallback

### Can't access from mobile?
- Check firewall settings
- Ensure both devices on same network
- Try using computer's IP address instead of localhost

### Service Worker not registering?
- Ensure you're accessing via HTTP/HTTPS (not file://)
- Check browser console for errors
- PWA features are optional, app works without them

## Security Notes

- Default server runs on all interfaces (0.0.0.0)
- For production, use proper authentication
- Add HTTPS for secure connections
- Implement rate limiting for API endpoints

## Next Steps

- Add user authentication
- Database integration for medication history
- SMS/WhatsApp notifications for caregivers
- Multi-user support
- Medication photo recognition
- Integration with pharmacy systems

---

**Need Help?** Check the main README.md or open an issue in the repository.

