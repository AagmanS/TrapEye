# LinkLens for WhatsApp - Verification Guide

## Prerequisites

1. FastAPI backend running on port 8002
2. Chrome browser with LinkLens extension installed
3. WhatsApp Web or test page open

## Verification Steps

### 1. Check Backend Health

Open a new terminal and run:
```bash
curl -Method GET -Uri "http://127.0.0.1:8002/health" -TimeoutSec 5
```

Expected response:
```json
{"status":"healthy","model_loaded":true,"service":"AI Phishing Detector"}
```

### 2. Test Backend Prediction

Run:
```bash
curl -Method POST -Uri "http://127.0.0.1:8002/predict" -Body '{"url":"https://google.com"}' -ContentType "application/json" -TimeoutSec 5
```

Expected response (similar):
```json
{"label":"safe","score":0.0,"reasons":[...],"explainability":[...]}
```

### 3. Verify Extension Installation

1. Open Chrome and go to `chrome://extensions`
2. Ensure "LinkLens for WhatsApp" is listed and enabled
3. Check that the extension icon appears in the toolbar

### 4. Test with Sample Page

1. Open [test_linklens.html](test_linklens.html) in Chrome
2. Open Developer Tools (F12)
3. Go to the Console tab
4. You should see:
   ```
   LinkLens for WhatsApp content script loaded
   Initializing LinkLens for WhatsApp
   ```
5. Check if link indicators appear next to the test links

### 5. Check Background Script

1. In `chrome://extensions`, find LinkLens for WhatsApp
2. Click "Inspect views: background.js"
3. In the new Developer Tools window, go to the Console tab
4. You should see:
   ```
   LinkLens for WhatsApp background service started
   ```

### 6. Test Popup Functionality

1. Click the LinkLens extension icon in the Chrome toolbar
2. The popup should appear with:
   - Title: "LinkLens for WhatsApp"
   - Connection status indicator
   - Instructions
   - "Scan Current Chat" button
   - "Extension Settings" button

### 7. Test with WhatsApp Web

1. Navigate to https://web.whatsapp.com
2. Scan a QR code to log in
3. Open any chat with links
4. Observe:
   - Links should be detected automatically
   - Indicators should appear next to links (green for safe, red for risky)
   - Floating panel button should appear in bottom right
   - Clicking the floating button should show the panel with analyzed links

### 8. Verify Caching

1. Analyze a link in WhatsApp Web
2. Note the result
3. Refresh the page or wait a few minutes
4. The same link should show the cached result immediately without backend call

## Troubleshooting

### If Extension Doesn't Load

1. Check that all files are in the `linklens-whatsapp` directory
2. Verify manifest.json is properly formatted
3. Reload the extension in `chrome://extensions`

### If Links Aren't Detected

1. Check Developer Tools console for errors
2. Verify WhatsApp Web DOM structure matches selectors
3. Try refreshing WhatsApp Web

### If Backend Connection Fails

1. Confirm backend is running on port 8002
2. Check network connectivity
3. Verify CORS settings in backend

### If Indicators Don't Appear

1. Check content.css is loaded properly
2. Verify content.js is running without errors
3. Ensure links match detection criteria

## Expected Behavior

### Safe Links (score < 0.5)
- Green indicator with "Safe" text
- Floating panel shows green "Safe" badge

### Risky Links (score >= 0.5)
- Red indicator with "Risky" text
- Floating panel shows red "Risky" badge

### Loading State
- Blue indicator with "Analyzing..." text

### Error State
- Gray indicator with "Error" text

## Success Criteria

✅ Extension installs without errors
✅ Backend connectivity verified
✅ Links detected in test page
✅ Visual indicators appear correctly
✅ Floating panel displays results
✅ Caching works properly
✅ Manual scan button functions
✅ Connection status shows correctly in popup

If all criteria are met, LinkLens for WhatsApp is working correctly!