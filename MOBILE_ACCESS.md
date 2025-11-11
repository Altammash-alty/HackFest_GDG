# How to Access MedMitra on Mobile Device

**Having voice recognition issues?** See [VOICE_TROUBLESHOOTING.md](VOICE_TROUBLESHOOTING.md) for solutions.

## Quick Steps

### Step 1: Find Your Computer's IP Address

**Windows:**
1. Open Command Prompt (Press `Win + R`, type `cmd`, press Enter)
2. Type: `ipconfig`
3. Look for **IPv4 Address** under your active network adapter
   - Example: `192.168.1.100` or `192.168.0.5`

**Mac:**
1. Open Terminal
2. Type: `ifconfig | grep "inet "`
3. Look for IP address starting with `192.168.` or `10.`
   - Example: `192.168.1.100`

**Linux:**
1. Open Terminal
2. Type: `ip addr` or `ifconfig`
3. Look for IP address under your network interface

### Step 2: Start the Server

On your computer, run:
```bash
python run_web.py
```

You should see:
```
🏥 MedMitra Web Server Starting...
🌐 Local:    http://localhost:5000
📱 Mobile:   http://<your-ip>:5000
```

### Step 3: Connect Mobile to Same Wi-Fi

- Make sure your mobile device is connected to the **same Wi-Fi network** as your computer
- Both devices must be on the same network (home Wi-Fi, office Wi-Fi, etc.)

### Step 4: Open on Mobile Browser

1. Open any browser on your mobile (Chrome, Safari, Firefox, etc.)
2. In the address bar, type:
   ```
   http://192.168.1.100:5000
   ```
   (Replace `192.168.1.100` with YOUR computer's IP address)
3. Press Go/Enter
4. The MedMitra app should load!

### Step 5: Install as App (Optional but Recommended)

**Android (Chrome):**
1. After the app loads, you'll see a prompt: "Add MedMitra to Home screen"
2. Tap "Add" or "Install"
3. Or: Tap menu (3 dots) → "Add to Home screen"

**iPhone/iPad (Safari):**
1. Tap the Share button (square with arrow pointing up)
2. Scroll down and tap "Add to Home Screen"
3. Tap "Add" in the top right
4. The app icon will appear on your home screen

**After Installation:**
- Tap the app icon to open MedMitra
- It works like a native app
- Works offline after first load
- No need to type the URL again

## Troubleshooting

### Can't Access from Mobile?

**Problem: Firewall blocking connection**
- **Windows:** Go to Windows Defender Firewall → Allow an app → Check Python
- Or temporarily disable firewall for testing

**Problem: Wrong IP address**
- Make sure you're using the IP address from the active network adapter
- If you have multiple network adapters (Wi-Fi, Ethernet), use the one that's connected

**Problem: Port 5000 not accessible**
- Try changing the port:
  ```bash
  # Windows PowerShell
  $env:PORT=8080
  python run_web.py
  ```
- Then access: `http://<your-ip>:8080`

**Problem: "This site can't be reached"**
- Check that server is running on computer
- Verify both devices on same Wi-Fi
- Try accessing from computer first: `http://localhost:5000`
- Check firewall settings

**Problem: Connection timeout**
- Make sure computer is not in sleep mode
- Keep the terminal window open (don't close it)
- Check that Python process is running

### Voice Not Working on Mobile?

**Grant Microphone Permission:**
- When browser asks for microphone access, tap "Allow"
- If denied, go to browser settings and enable microphone for the site

**Browser Compatibility:**
- **Best:** Chrome (Android), Safari (iOS)
- **Good:** Edge, Firefox
- Voice features work best on Chrome and Safari

### Keep App Running

**To keep reminders working:**
- Keep the browser tab open (don't close it)
- Keep the computer running (don't put to sleep)
- Keep the server running (don't close terminal)

**For 24/7 operation:**
- Consider running on a Raspberry Pi or always-on computer
- Or use a cloud service (Heroku, Railway, etc.)

## Alternative: Use Your Computer's Name

Some networks allow accessing by computer name:

**Windows:**
- Access via: `http://YourComputerName:5000`
- Find computer name: Settings → System → About

**Mac:**
- Access via: `http://YourMacName.local:5000`
- Find computer name: System Preferences → Sharing

## Quick Reference

```
Computer IP: 192.168.1.100 (example)
Mobile URL:  http://192.168.1.100:5000
Port:        5000 (default)
Network:     Same Wi-Fi required
```

## Need Help?

1. Check server is running (see terminal output)
2. Verify IP address is correct
3. Ensure same Wi-Fi network
4. Try accessing from computer first
5. Check firewall settings

---

**Pro Tip:** After installing as PWA, you can access MedMitra just like any other app on your phone - no browser needed!

