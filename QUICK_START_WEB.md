# MedMitra Web - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web server)
- Flask-SocketIO (real-time communication)
- Flask-CORS (cross-origin support)
- Eventlet (async server)

### Step 2: Start the Server

```bash
python run_web.py
```

You'll see:
```
🏥 MedMitra Web Server Starting...
🌐 Local:    http://localhost:5000
📱 Mobile:   http://<your-ip>:5000
```

### Step 3: Open in Browser

**On your computer:**
- Open browser and go to: `http://localhost:5000`

**On your mobile device:**
1. Find your computer's IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `ip addr`
2. Make sure mobile is on same Wi-Fi network
3. Open browser on mobile
4. Go to: `http://<your-ip>:5000`
   - Example: `http://192.168.1.100:5000`

## 🎤 Using Voice Features

1. **Grant microphone permission** when browser asks
2. **Tap the microphone button** (large green button)
3. **Speak your response** in Hindi or English
4. MedMitra will respond with voice output

## 📱 Install as App (PWA)

**Android:**
- Chrome will show "Add to Home Screen" prompt
- Or: Menu → "Add to Home Screen"

**iOS:**
- Tap Share button (square with arrow)
- Select "Add to Home Screen"

After installation, the app works offline!

## 🎯 Features

✅ **Automatic Reminders** - Triggers at exact prescribed times  
✅ **Voice Input** - Speak naturally in Hindi/English  
✅ **Voice Output** - MedMitra speaks responses  
✅ **Auto Voice Listening** - Starts automatically after reminders  
✅ **Smart Recognition** - Understands "Haan"/"Nahi" and variations  
✅ **Real-time Tracking** - Records medication intake automatically  
✅ **Mobile Optimized** - Large buttons, easy to use  
✅ **Offline Support** - Works after first load  
✅ **Cross-Platform** - iOS, Android, Desktop

## 🔔 How Automatic Reminders Work

1. **Server runs continuously** - Checks every 30 seconds for due medications
2. **Reminder appears automatically** - Pulsing red card at scheduled time
3. **MedMitra speaks** - Reminder is spoken aloud
4. **Voice listening starts** - Automatically after 3 seconds
5. **User responds** - Simply say "Haan" (Yes) or "Nahi" (No)
6. **System records** - Medication status tracked automatically

See [AUTOMATIC_REMINDERS.md](AUTOMATIC_REMINDERS.md) for detailed information.  

## 🔧 Troubleshooting

**Voice not working?**
- Check browser compatibility (Chrome/Safari recommended)
- Grant microphone permissions
- Use text input as fallback

**Can't access from mobile?**
- Check firewall settings
- Ensure same Wi-Fi network
- Try computer's IP instead of localhost

**Port already in use?**
```bash
# Change port
$env:PORT=8080  # Windows PowerShell
python run_web.py
```

## 📚 More Information

- Full setup: [WEB_SETUP.md](WEB_SETUP.md)
- Main README: [README.md](README.md)

---

**Ready to use!** The app is now running and accessible from any device. 🎉

