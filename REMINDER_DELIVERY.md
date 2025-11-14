# 🔔 How Medication Reminders Work

## ✅ Yes, Linked Devices Receive Reminders!

When you link a patient's mobile device, **it WILL receive medication reminders** automatically at the scheduled times.

---

## 📱 How It Works

### **Reminder Delivery System:**

1. **Server Checks Every 60 Seconds**
   - The server continuously monitors for medications due at the current time
   - Checks happen automatically in the background

2. **Reminder Sent via WebSocket**
   - When a medication is due, the server sends a reminder to **all connected devices**
   - Uses real-time WebSocket connection for instant delivery

3. **Patient App Receives Reminder**
   - Reminder appears as a **pulsing card** on the screen
   - **Voice announcement** plays automatically
   - **Browser notification** appears (if permission granted)
   - **Device vibrates** (if supported)

4. **Patient Responds**
   - Patient says **"Haan"** (Yes) or **"Nahi"** (No)
   - Response is recorded and sent to caregiver dashboard

---

## ⚠️ Important Requirements

### **For Reminders to Work:**

✅ **Patient app must be open** (browser tab or installed app)
✅ **WebSocket connection active** (automatic when app is open)
✅ **Same Wi-Fi network** (patient phone and server computer)
✅ **Server must be running** (keep terminal window open)

### **What Happens If App is Closed:**

❌ **Reminders won't be received** if:
- Browser tab is closed
- App is not running
- Phone is offline
- WebSocket connection is lost

---

## 🔔 Browser Notifications (Background Alerts)

The system now includes **browser notifications** that work even when the app is in the background:

### **How to Enable:**

1. When patient first opens the app, browser will ask for **notification permission**
2. Patient must tap **"Allow"** or **"Permit"**
3. Notifications will now appear even if app is in background

### **What Notifications Show:**

- 🔔 Medication name and dosage
- ⏰ Reminder that it's time to take medication
- 📱 Appears on lock screen (mobile)
- 🔊 Can play sound/vibration

### **Notification Settings:**

**Android (Chrome):**
- Settings → Site Settings → Notifications → Allow

**iPhone (Safari):**
- Settings → Safari → Notifications → Allow

---

## 💡 Best Practices for Reliable Reminders

### **For Patient:**

1. **Install as PWA** (Progressive Web App)
   - Add to home screen for easy access
   - App stays active longer

2. **Keep App Open**
   - Don't close the browser tab
   - Keep app running in background

3. **Grant Permissions**
   - Allow microphone (for voice responses)
   - Allow notifications (for background alerts)

4. **Keep Phone Charged**
   - Ensure phone doesn't go to sleep
   - Disable battery optimization for browser

### **For Caregiver:**

1. **Keep Server Running**
   - Don't close the terminal window
   - Keep computer awake (disable sleep mode)

2. **Monitor Connection**
   - Check dashboard to see if patient is connected
   - Verify reminders are being sent

3. **Test Reminders**
   - Set a test medication for a few minutes ahead
   - Verify patient receives reminder

---

## 🔄 Connection Status

### **How to Check if Patient is Connected:**

1. Open **Caregiver Dashboard** (`/dashboard`)
2. Check the **History** tab
3. If patient is connected, you'll see real-time updates

### **Connection Indicators:**

- **Green dot** = Connected ✅
- **Red dot** = Disconnected ❌
- **Pulsing dot** = Connecting...

---

## 📊 Reminder Schedule

Reminders are sent at these default times:

- **Morning:** 8:00 AM
- **Afternoon:** 2:00 PM
- **Evening:** 6:00 PM
- **Night:** 9:00 PM

*Times can be customized when adding medications in the dashboard.*

---

## 🛠️ Troubleshooting Reminders

### **Patient Not Receiving Reminders?**

**Check:**
1. ✅ Is server running? (Check terminal window)
2. ✅ Is patient app open? (Browser tab must be open)
3. ✅ Same Wi-Fi network? (Both devices on same network)
4. ✅ WebSocket connected? (Check status indicator - should be green)
5. ✅ Medication scheduled? (Check dashboard - Medications tab)

### **Reminders Not Appearing?**

**Try:**
1. Refresh patient app (pull down to refresh)
2. Check browser console for errors
3. Verify medication time matches current time
4. Check if reminder was already sent today

### **Notifications Not Working?**

**Enable:**
1. Grant notification permission in browser
2. Check phone notification settings
3. Ensure browser notifications are enabled
4. Try different browser (Chrome/Safari recommended)

---

## 🎯 Summary

**YES, linked devices receive reminders!**

✅ Reminders are sent automatically at scheduled times
✅ Works via WebSocket for real-time delivery
✅ Browser notifications work in background
✅ Patient can respond with voice or text
✅ Caregiver sees all responses in dashboard

**Requirements:**
- Patient app must be open (or notifications enabled)
- Server must be running
- Same Wi-Fi network
- WebSocket connection active

---

## 💬 Quick Answer

**Q: Will the linked device get reminders?**
**A: YES!** As long as:
- The patient app is open in the browser
- The server is running
- Both devices are on the same Wi-Fi network

**For best results:** Install as PWA and grant notification permissions for background reminders!

---

**Need help?** Check the dashboard History tab to see if reminders are being delivered and recorded.

