# 📱 Patient Mobile Setup Guide

## Quick Setup for Patient's Mobile Device

This guide shows you how to connect a patient's mobile phone to MedMitra so they can receive medication reminders and respond with "Haan" (Yes) or "Nahi" (No).

---

## 🎯 Two Ways to Set Up Patient Mobile

### **Method 1: Direct Link (Easiest)**
Share a link that the patient can open on their phone.

### **Method 2: QR Code (Recommended)**
Generate a QR code that the patient can scan.

---

## 📋 Step-by-Step Setup

### **Step 1: Start the Server**

On your computer (caregiver's computer), run:

```bash
python run_web.py
```

You'll see output like:
```
🏥 MedMitra Web Server Starting...
🌐 Local:    http://localhost:5000
📱 Mobile:   http://192.168.1.100:5000
```

**Note the IP address** shown (e.g., `192.168.1.100`)

---

### **Step 2: Find Your Computer's IP Address**

If the IP isn't shown, find it manually:

**Windows:**
1. Press `Win + R`, type `cmd`, press Enter
2. Type: `ipconfig`
3. Look for **IPv4 Address** (e.g., `192.168.1.100`)

**Mac:**
1. Open Terminal
2. Type: `ifconfig | grep "inet "`
3. Look for IP starting with `192.168.` or `10.`

**Linux:**
1. Open Terminal
2. Type: `ip addr` or `ifconfig`
3. Find your network IP address

---

### **Step 3: Get the Patient App Link**

The patient app URL is:
```
http://<YOUR_IP_ADDRESS>:5000
```

**Example:**
```
http://192.168.1.100:5000
```

**For Dashboard (Caregiver):**
```
http://192.168.1.100:5000/dashboard
```

---

### **Step 4: Share Link with Patient**

**Option A: Send via WhatsApp/Message**
1. Copy the patient app link: `http://192.168.1.100:5000`
2. Send it to the patient via WhatsApp, SMS, or email
3. Patient clicks the link to open

**Option B: Show on Screen**
1. Display the link on your computer screen
2. Patient types it into their mobile browser

**Option C: Use QR Code (See below)**

---

### **Step 5: Patient Opens Link on Mobile**

1. Patient opens **Chrome** or **Safari** on their phone
2. Types or pastes: `http://192.168.1.100:5000`
3. Presses **Go** or **Enter**
4. MedMitra patient app loads! 🎉

---

### **Step 6: Install as App (Recommended)**

After the app loads, patient should install it on their home screen:

**Android (Chrome):**
1. Tap menu (3 dots) → **"Add to Home screen"**
2. Or look for **"Install"** prompt
3. Tap **"Add"** or **"Install"**

**iPhone/iPad (Safari):**
1. Tap **Share** button (square with arrow ↑)
2. Scroll down and tap **"Add to Home Screen"**
3. Tap **"Add"** in top right

**After Installation:**
- Patient can tap the app icon to open MedMitra
- Works like a native app
- No need to type URL again
- Works even when offline (after first load)

---

## 🔗 Using Dashboard to Share Link

1. Open caregiver dashboard: `http://<YOUR_IP>:5000/dashboard`
2. Go to **"Patient View"** tab
3. Copy the link shown
4. Share with patient via WhatsApp/email/SMS

---

## 📱 QR Code Method (Easiest for Patient)

### Generate QR Code:

1. **Online QR Generator:**
   - Go to: https://www.qr-code-generator.com/
   - Enter patient app URL: `http://192.168.1.100:5000`
   - Generate QR code
   - Download and share with patient

2. **Python Script (if you have qrcode library):**
   ```bash
   pip install qrcode[pil]
   python -c "import qrcode; qr = qrcode.QRCode(); qr.add_data('http://192.168.1.100:5000'); qr.make(); img = qr.make_image(); img.save('patient_link.png')"
   ```

3. **Share QR Code:**
   - Print it out
   - Send via WhatsApp/email
   - Display on screen
   - Patient scans with phone camera

---

## ✅ Important Requirements

### **Same Wi-Fi Network**
- Patient's phone and your computer must be on the **same Wi-Fi network**
- Both devices must be connected to the same router

### **Server Must Be Running**
- Keep the terminal window open on your computer
- Don't close the server (don't press Ctrl+C)
- Computer should not be in sleep mode

### **Firewall Settings**
- Windows Firewall might block connections
- Allow Python through firewall when prompted
- Or temporarily disable firewall for testing

---

## 🎤 Grant Microphone Permission

When patient first opens the app:
1. Browser will ask for **microphone permission**
2. Patient must tap **"Allow"** or **"Permit"**
3. This enables voice input for "Haan"/"Nahi" responses

**If denied:**
- Android Chrome: Settings → Site Settings → Microphone → Allow
- iPhone Safari: Settings → Safari → Microphone → Allow

---

## 🔄 How It Works

1. **Caregiver sets up medications** in dashboard (`/dashboard`)
2. **Patient receives reminders** on their mobile app (`/`)
3. **Reminder appears** at scheduled time with:
   - Medication name and dosage
   - Simple explanation of why they're taking it
   - Voice prompt asking "Haan" or "Nahi"
4. **Patient responds** by voice or text
5. **Caregiver sees response** in dashboard history

---

## 🛠️ Troubleshooting

### **Patient Can't Connect**

**Problem:** "This site can't be reached"
- ✅ Check server is running on your computer
- ✅ Verify both devices on same Wi-Fi
- ✅ Try accessing from your computer first: `http://localhost:5000`
- ✅ Check firewall settings

**Problem:** Wrong IP address
- ✅ Run `ipconfig` (Windows) or `ifconfig` (Mac/Linux) again
- ✅ Use the IP from the active network adapter
- ✅ If IP changed, share new link with patient

**Problem:** Connection timeout
- ✅ Make sure computer is not in sleep mode
- ✅ Keep terminal window open
- ✅ Check that Python process is running

### **Voice Not Working on Patient's Phone**

**Problem:** Microphone not working
- ✅ Grant microphone permission when browser asks
- ✅ Use Chrome (Android) or Safari (iOS) for best results
- ✅ Check browser settings → Microphone → Allow
- ✅ Patient can use text input as fallback

**Problem:** Voice recognition not accurate
- ✅ Patient should speak clearly
- ✅ Say "Haan" (Yes) or "Nahi" (No) clearly
- ✅ Can also type response in text box

---

## 📍 Quick Reference

```
Patient App URL:  http://<YOUR_IP>:5000
Dashboard URL:    http://<YOUR_IP>:5000/dashboard
Default Port:     5000
Network:          Same Wi-Fi required
```

**Example:**
- Your IP: `192.168.1.100`
- Patient app: `http://192.168.1.100:5000`
- Dashboard: `http://192.168.1.100:5000/dashboard`

---

## 💡 Pro Tips

1. **Install as PWA:** Patient should install app on home screen for easy access
2. **Keep Server Running:** Don't close terminal window
3. **Same Network:** Both devices must be on same Wi-Fi
4. **Test First:** Try accessing from your computer before sharing with patient
5. **QR Code:** Easiest way for patient to access - just scan and open

---

## 🆘 Need Help?

1. ✅ Check server is running (see terminal output)
2. ✅ Verify IP address is correct
3. ✅ Ensure same Wi-Fi network
4. ✅ Try accessing from computer first
5. ✅ Check firewall settings
6. ✅ Make sure patient granted microphone permission

---

## 📞 Summary

**For Caregiver:**
1. Run `python run_web.py` on your computer
2. Note the IP address shown
3. Share link: `http://<IP>:5000` with patient
4. Monitor responses in dashboard: `http://<IP>:5000/dashboard`

**For Patient:**
1. Open link on mobile browser
2. Install as app (add to home screen)
3. Grant microphone permission
4. Wait for medication reminders
5. Respond with "Haan" or "Nahi"

---

**That's it!** Once set up, the patient will receive automatic medication reminders and you can monitor their responses in real-time through the dashboard. 🎉

