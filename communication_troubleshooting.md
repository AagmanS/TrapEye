# LinkLens for WhatsApp - Communication Error Troubleshooting

## Error: "Error sending message to content script"

This error occurs when the background script cannot communicate with the content script. Here are the most common causes and solutions:

## 🔍 Common Causes

### 1. Content Script Not Loaded
The content script may not be loaded on the current page.

**Solution:**
- Ensure you're on https://web.whatsapp.com
- Refresh the page
- Check that the extension is enabled for this site

### 2. Tab ID Issues
The tab ID may be invalid or the tab may have been closed.

**Solution:**
- Make sure WhatsApp Web is open in an active tab
- Try closing and reopening WhatsApp Web
- Restart Chrome if the issue persists

### 3. Timing Issues
The content script may not be ready when the message is sent.

**Solution:**
- The extension now includes better error handling for this case
- No user action needed - errors are logged but don't break functionality

### 4. Permissions Issues
The extension may not have proper permissions for the current site.

**Solution:**
- Go to `chrome://extensions`
- Click "Details" for LinkLens
- Ensure "Access to web.whatsapp.com" is allowed

## 🛠️ Diagnostic Steps

### Step 1: Check Extension Permissions
1. Open Chrome and go to `chrome://extensions`
2. Find "LinkLens for WhatsApp"
3. Click the "Details" button
4. Scroll down to "Site access"
5. Ensure "On web.whatsapp.com" is set to "On"

### Step 2: Verify Content Script Loading
1. Open WhatsApp Web (https://web.whatsapp.com)
2. Press F12 to open Developer Tools
3. Go to the Console tab
4. Look for the message: "LinkLens for WhatsApp content script loaded"
5. If you don't see this message, the content script isn't loading

### Step 3: Test Background Script
1. In `chrome://extensions`, find LinkLens
2. Click "Inspect views: background.js"
3. Check the Console tab for errors
4. Look for "LinkLens for WhatsApp background service started"

### Step 4: Check Network Connectivity
1. Verify the FastAPI backend is running on port 8002
2. Test the health endpoint:
   ```bash
   curl http://127.0.0.1:8002/health
   ```
3. You should get a response like:
   ```json
   {"status":"healthy","model_loaded":true,"service":"AI Phishing Detector"}
   ```

## 🛠️ Advanced Troubleshooting

### Clear Extension Data
1. Open Chrome Developer Tools on WhatsApp Web
2. Go to Application tab
3. Under Storage, click "Clear storage"
4. Refresh the page

### Reload Extension
1. In `chrome://extensions`, click the reload icon on the LinkLens card
2. Refresh WhatsApp Web

### Check for Conflicting Extensions
1. Disable other Chrome extensions temporarily
2. Test LinkLens again
3. Re-enable extensions one by one to identify conflicts

## 📊 Error Logging Improvements

The updated extension now provides more detailed error logging:

### Background Script Logs
```
Error sending message to content script: [error details]
Tab ID: [tab ID]
URL being scanned: [URL]
```

### Content Script Logs
```
Error sending message to background: [error details]
URL that failed to send: [URL]
```

## 🎯 Success Indicators

When the extension is working properly, you should see:

1. **In Background Script Console:**
   - "LinkLens for WhatsApp background service started"
   - "Received message in background: [message details]"
   - "Scanning URL with FastAPI backend: [URL]"
   - "API response: [response details]"

2. **In Content Script Console:**
   - "LinkLens for WhatsApp content script loaded"
   - "Initializing LinkLens for WhatsApp"
   - "Scanning for links..."
   - "Sending URL for scanning: [URL]"
   - "Handling scan result for [URL]: [result details]"

3. **In WhatsApp Web:**
   - Links should have colored indicators (green for safe, red for risky)
   - Floating panel button in bottom right corner
   - Clicking links should show analysis details

## 🔄 Error Handling Improvements

The updated extension handles communication errors gracefully:

1. **Non-Critical Errors:** Communication errors are logged but don't break the extension
2. **Retry Logic:** Failed scans are marked with error indicators
3. **User Feedback:** Clear visual indicators for different states
4. **Detailed Logging:** More specific error messages for debugging

## 📞 Support

If you continue to experience communication issues:

1. Take screenshots of the error messages
2. Include console logs from both background and content scripts
3. Provide details about your environment:
   - Chrome version
   - Operating system
   - Extension version
   - Backend status

4. Try the communication test page: [communication_test.html](communication_test.html)