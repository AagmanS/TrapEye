# LinkLens for WhatsApp - Troubleshooting Guide

## Common Issues and Solutions

### 1. "Error initiating scan. Please make sure WhatsApp Web is open."

This error occurs when the extension cannot communicate with WhatsApp Web. Here are the steps to fix it:

#### Check if WhatsApp Web is properly loaded:
1. Make sure you're on https://web.whatsapp.com
2. Ensure the page has fully loaded (QR code scanner or chat interface visible)
3. If you see a QR code, scan it with your phone to log in

#### Check if the extension is properly loaded:
1. Go to `chrome://extensions`
2. Make sure "LinkLens for WhatsApp" is enabled
3. Click the refresh icon on the extension card
4. Reload WhatsApp Web page (Ctrl+R or F5)

#### Check console for errors:
1. On WhatsApp Web, press F12 to open Developer Tools
2. Go to the Console tab
3. Look for any error messages related to LinkLens
4. If you see "LinkLens for WhatsApp content script loaded", the extension is working

### 2. Links are not being detected

#### Check CSS selectors:
The extension uses specific CSS selectors to find messages. If WhatsApp Web updates its UI, these selectors might need updating:

Current selectors:
- `[data-testid="msg-container"]`
- `.message-in`
- `.message-out`
- `[class*="message"]`
- `.copyable-text`

#### Manual trigger:
1. Click the LinkLens extension icon in the Chrome toolbar
2. Click "Scan Current Chat" button
3. Check if links are detected after manual trigger

### 3. Backend connection issues

#### Verify backend is running:
1. Open a terminal/command prompt
2. Run: `curl -Method GET -Uri "http://127.0.0.1:8002/health" -TimeoutSec 5`
3. You should get a response like: `{"status":"healthy","model_loaded":true,"service":"AI Phishing Detector"}`

#### Check backend port:
The extension expects the backend on port 8002. If your backend runs on a different port:
1. Edit `content.js` and `background.js`
2. Change `http://127.0.0.1:8002/predict` to your actual port
3. Edit `manifest.json` to update host permissions
4. Reload the extension

### 4. Indicators not appearing

#### Check content.css:
1. Go to `chrome://extensions`
2. Find LinkLens for WhatsApp
3. Click "Inspect views: content.css"
4. Check if there are any loading errors

#### Check z-index issues:
The floating panel uses z-index: 10000. If WhatsApp Web elements have higher z-index values, they might overlap the panel.

### 5. Caching issues

#### Clear cache:
1. Open Chrome Developer Tools on WhatsApp Web
2. Go to Application tab
3. Under Storage, click "Clear storage"
4. Or specifically clear IndexedDB and Local Storage

### 6. Extension not loading

#### Check manifest errors:
1. Go to `chrome://extensions`
2. Enable "Developer mode"
3. Look for any error messages under LinkLens extension

#### Reload extension:
1. In `chrome://extensions`, click the reload icon on the LinkLens card
2. Refresh WhatsApp Web page

## Debugging Steps

### 1. Check content script logs:
1. On WhatsApp Web, press F12 to open Developer Tools
2. Go to Console tab
3. Look for messages starting with "LinkLens"

### 2. Check background script logs:
1. Go to `chrome://extensions`
2. Find LinkLens for WhatsApp
3. Click "Inspect views: background.js"
4. Check Console tab for errors

### 3. Check popup logs:
1. Click the LinkLens extension icon
2. Right-click on the popup
3. Select "Inspect"
4. Check Console tab

### 4. Test API directly:
1. Open terminal/command prompt
2. Run: `curl -Method POST -Uri "http://127.0.0.1:8002/predict" -Body '{"url":"https://google.com"}' -ContentType "application/json" -TimeoutSec 5`
3. Verify you get a proper response

## Advanced Troubleshooting

### Update CSS selectors:
If WhatsApp Web updates its UI, update the selectors in `content.js`:
```javascript
const messageSelectors = [
  '[data-testid="msg-container"]',
  '.message-in',
  '.message-out',
  // Add new selectors here
];
```

### Check permissions:
Ensure `manifest.json` has the correct permissions:
```json
"host_permissions": [
  "http://127.0.0.1:8002/*",
  "https://web.whatsapp.com/*"
]
```

### Network issues:
If there are network connectivity issues:
1. Check firewall settings
2. Verify localhost is not blocked
3. Try accessing http://127.0.0.1:8002/health in browser directly

## Contact Support

If none of these solutions work:
1. Take screenshots of error messages
2. Include console logs from both content script and background script
3. Provide details about your environment (Chrome version, OS, etc.)