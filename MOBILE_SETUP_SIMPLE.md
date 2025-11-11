# 📱 How to Open MedMitra on Your Mobile - Simple Guide

## Your Computer's IP Address
**Your IP:** `172.18.40.183` (found automatically)

## 3 Simple Steps

### Step 1: Start the Server
On your computer, run:
```bash
python run_web.py
```

Or double-click: `START_MOBILE.bat` (Windows)

### Step 2: Connect Mobile to Same Wi-Fi
- Make sure your phone is on the **same Wi-Fi network** as your computer
- Both must be connected to the same router/network

### Step 3: Open on Mobile Browser
1. Open **Chrome** or **Safari** on your phone
2. Type this in the address bar:
   ```
   http://172.18.40.183:5000
   ```
3. Press **Go** or **Enter**
4. MedMitra will load! 🎉

## Install as App (Recommended)

After the app loads:

**Android:**
- Tap the menu (3 dots) → "Add to Home screen"
- Or look for "Install" prompt

**iPhone:**
- Tap Share button (square with arrow) → "Add to Home Screen"

Now you can open MedMitra like any other app!

## Quick Test

1. ✅ Server running? (Check terminal window)
2. ✅ Same Wi-Fi? (Phone and computer)
3. ✅ Type URL: `http://172.18.40.183:5000`
4. ✅ Press Go!

## Troubleshooting

**Can't connect?**
- Make sure server is running (terminal window open)
- Check both devices on same Wi-Fi
- Try: `http://localhost:5000` on computer first
- Windows Firewall might block - allow Python through firewall

**IP address changed?**
- Run `ipconfig` (Windows) to get new IP
- Or use `START_MOBILE.bat` to see current IP

**Voice not working?**
- Grant microphone permission when browser asks
- Use Chrome (Android) or Safari (iOS) for best results

---

**That's it!** Once installed, just tap the app icon to open MedMitra.

