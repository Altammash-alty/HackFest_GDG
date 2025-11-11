# Voice Recognition Troubleshooting Guide

## Common Voice Recognition Errors on Mobile

### Error: "Microphone permission denied" / "not-allowed"

**Solution:**
1. **Chrome (Android):**
   - Tap the lock icon in address bar
   - Tap "Site settings"
   - Find "Microphone" → Change to "Allow"
   - Reload the page

2. **Safari (iOS):**
   - Go to Settings → Safari → Microphone
   - Enable for the site
   - Or: Settings → Privacy → Microphone → Enable Safari

3. **General:**
   - When browser asks for microphone permission, tap "Allow"
   - If you denied earlier, you need to enable it in browser settings

### Error: "No speech detected" / "no-speech"

**Solutions:**
- Speak louder and clearer
- Move closer to microphone
- Check microphone is working (test in other apps)
- Reduce background noise
- Wait for "Listening..." to appear before speaking

### Error: "Network error" / "network"

**Solutions:**
- Check internet connection
- Web Speech API requires internet connection
- Try refreshing the page
- Check if firewall is blocking the connection

### Error: "Service not allowed" / "service-not-allowed"

**Cause:** Some browsers require HTTPS for voice recognition

**Solutions:**
1. **Use HTTPS (Recommended):**
   - Deploy to a service with HTTPS (Heroku, Railway, etc.)
   - Or use ngrok for local HTTPS: `ngrok http 5000`

2. **Use Text Input:**
   - Voice may not work on HTTP connections
   - Text input always works as fallback

### Error: "Language not supported"

**Solutions:**
- The app will automatically fallback to English
- Try speaking in English if Hindi doesn't work
- Check browser language settings

## Browser Compatibility

### ✅ Fully Supported:
- **Chrome (Android)** - Best support
- **Safari (iOS 14.5+)** - Good support
- **Chrome (Desktop)** - Excellent support
- **Edge (Mobile/Desktop)** - Good support

### ⚠️ Limited Support:
- **Firefox** - Limited voice recognition
- **Samsung Internet** - May have issues

### ❌ Not Supported:
- **Older browsers** - Use text input instead

## Mobile-Specific Tips

### Android:
1. **Grant Permissions:**
   - Settings → Apps → Browser → Permissions → Microphone → Allow

2. **Use Chrome:**
   - Chrome has best voice recognition support
   - Other browsers may have issues

3. **Check System Settings:**
   - Settings → Apps → Browser → Microphone → Enable

### iOS:
1. **Safari Only:**
   - Voice recognition works best in Safari
   - Chrome on iOS has limited support

2. **iOS Settings:**
   - Settings → Safari → Microphone → Allow
   - Settings → Privacy → Microphone → Enable Safari

3. **iOS Version:**
   - Requires iOS 14.5 or later for best support

## Quick Fixes

### Fix 1: Reload and Grant Permission
1. Reload the page
2. When asked for microphone permission, tap "Allow"
3. Try voice input again

### Fix 2: Clear Browser Data
1. Go to browser settings
2. Clear site data/cookies for the MedMitra site
3. Reload and grant permission again

### Fix 3: Use Text Input
- If voice doesn't work, use the text input field
- All features work with text input too
- Type "Haan" or "Nahi" to respond

### Fix 4: Check HTTPS
- Voice recognition may require HTTPS
- If using HTTP locally, consider:
  - Using ngrok: `ngrok http 5000`
  - Deploying to cloud service with HTTPS

## Testing Voice Recognition

1. **Test Microphone:**
   - Open any voice recording app
   - Record and play back to verify microphone works

2. **Test Browser:**
   - Try voice search in Google
   - If that works, MedMitra should work too

3. **Test Permissions:**
   - Open browser settings
   - Check microphone permission is enabled

## Still Not Working?

1. **Check Console:**
   - Open browser developer tools (F12)
   - Check Console tab for error messages
   - Share error code for help

2. **Try Different Browser:**
   - Chrome (Android) or Safari (iOS) recommended
   - Some browsers have better support

3. **Use Text Input:**
   - All features work with text
   - Type responses instead of speaking
   - Works on all devices and browsers

4. **Check Server:**
   - Make sure server is running
   - Check WebSocket connection (green status indicator)

## Error Codes Reference

| Error Code | Meaning | Solution |
|------------|---------|----------|
| `no-speech` | No voice detected | Speak louder, check microphone |
| `aborted` | Recognition stopped | Try again |
| `audio-capture` | Microphone not found | Check permissions |
| `network` | Network error | Check internet connection |
| `not-allowed` | Permission denied | Enable microphone in settings |
| `service-not-allowed` | Service blocked | May need HTTPS |
| `bad-grammar` | Grammar error | Try speaking again |
| `language-not-supported` | Language issue | Will fallback to English |

## Best Practices

1. **Grant Permission Once:**
   - Allow microphone when first asked
   - Browser will remember your choice

2. **Speak Clearly:**
   - Speak at normal volume
   - Wait for "Listening..." before speaking
   - Reduce background noise

3. **Use Supported Browsers:**
   - Chrome (Android) or Safari (iOS)
   - Best compatibility and features

4. **Keep Browser Updated:**
   - Latest browsers have better support
   - Update browser regularly

---

**Remember:** Text input always works as a reliable fallback if voice recognition has issues!

