# LinkLens for WhatsApp Installation Guide

## Prerequisites

1. Make sure the FastAPI backend is running on port 8002
2. Google Chrome browser

## Installation Steps

1. Open Google Chrome
2. Navigate to `chrome://extensions`
3. Enable "Developer mode" by toggling the switch in the top right corner
4. Click the "Load unpacked" button
5. Select the `linklens-whatsapp` folder from your project directory
6. The extension should now be installed and visible in your Chrome toolbar

## Starting the Backend

If the backend is not running, start it with:

```bash
cd backend
python main.py
```

Or if you're using the provided start script:

```bash
python start_server.py
```

## Testing the Extension

1. Open the test page by navigating to the [test_linklens.html](test_linklens.html) file in your browser
2. The extension should automatically detect and analyze the links on the page
3. Safe links will be marked with a green indicator
4. Risky links will be marked with a red indicator

## Using with WhatsApp Web

1. Navigate to https://web.whatsapp.com
2. Open any chat containing links
3. The extension will automatically analyze all links in the chat
4. Results will be displayed next to each link
5. Click the floating LinkLens button in the bottom right to open the results panel

## Troubleshooting

If the extension isn't working:

1. Check that the FastAPI backend is running on port 8002
2. Verify the backend health endpoint: http://127.0.0.1:8002/health
3. Check the Chrome extension console for error messages:
   - Right-click on the extension icon
   - Select "Manage Extensions"
   - Click "Inspect views: background.js" to see background logs
   - On WhatsApp Web, open Developer Tools (F12) to see content script logs
4. Make sure the extension has the necessary permissions
5. Try refreshing WhatsApp Web or restarting the browser