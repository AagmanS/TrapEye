# LinkLens for WhatsApp - sendMessage Error Troubleshooting

## Error: Issues with `chrome.runtime.sendMessage`

This error occurs when there are problems with message passing between the content script and background script. Here are the most common causes and solutions:

## 🔍 Common Causes

### 1. Extension Not Loaded Properly
The extension may not be loaded or enabled correctly.

**Solution:**
- Go to `chrome://extensions`
- Ensure LinkLens is enabled
- Click the reload icon if it's already enabled
- Check for any error messages

### 2. Background Script Not Running
The background service worker may have stopped or crashed.

**Solution:**
- In `chrome://extensions`, click "Inspect views: background.js"
- Check the Console tab for errors
- Look for "LinkLens for WhatsApp background service started"

### 3. Content Script Context Issues
The content script may be running in an incorrect context.

**Solution:**
- Check that you're on https://web.whatsapp.com
- Refresh the page
- Check the Console tab for "LinkLens for WhatsApp content script loaded"

### 4. Message Format Issues
The message format may be incorrect or missing required fields.

**Solution:**
- Ensure messages have the correct structure:
  ```javascript
  {
    action: 'scanUrl',
    url: 'https://example.com'
  }
  ```

## 🛠️ Diagnostic Steps

### Step 1: Verify Extension Loading
1. Open Chrome and go to `chrome://extensions`
2. Find "LinkLens for WhatsApp"
3. Ensure it's enabled (toggle is on)
4. Click the reload icon
5. Check for any error messages

### Step 2: Check Background Script
1. In `chrome://extensions`, find LinkLens
2. Click "Inspect views: background.js"
3. Check the Console tab
4. Look for "LinkLens for WhatsApp background service started"
5. Check for any error messages

### Step 3: Check Content Script
1. Open WhatsApp Web (https://web.whatsapp.com)
2. Press F12 to open Developer Tools
3. Go to the Console tab
4. Look for "LinkLens for WhatsApp content script loaded"
5. Check for any error messages

### Step 4: Test Message Passing
1. Open the [send_message_test.html](send_message_test.html) file
2. Click the various test buttons
3. Check the log for results
4. Look for any error messages

## 🛠️ Advanced Troubleshooting

### Clear Extension Data
1. Open Chrome Developer Tools on WhatsApp Web
2. Go to Application tab
3. Under Storage, click "Clear storage"
4. Refresh the page

### Check Manifest Configuration
1. Open `linklens-whatsapp/manifest.json`
2. Verify the background script is correctly configured:
   ```json
   "background": {
     "service_worker": "background.js"
   }
   ```
3. Verify content script matches:
   ```json
   "content_scripts": [
     {
       "matches": ["https://web.whatsapp.com/*"],
       "js": ["content.js"],
       "css": ["content.css"]
     }
   ]
   ```

### Test with Minimal Example
Create a simple test to isolate the issue:

1. Create a minimal content script:
   ```javascript
   chrome.runtime.sendMessage({action: 'test'}, (response) => {
     if (chrome.runtime.lastError) {
       console.error('Error:', chrome.runtime.lastError);
     } else {
       console.log('Response:', response);
     }
   });
   ```

2. Add a handler in the background script:
   ```javascript
   chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
     if (request.action === 'test') {
       sendResponse({status: 'success'});
     }
   });
   ```

## 📊 Error Handling Improvements

The updated extension now provides better error handling:

### Content Script Error Handling
```javascript
try {
  chrome.runtime.sendMessage({
    action: 'scanUrl',
    url: url
  }, (response) => {
    // Handle response if needed
    if (chrome.runtime.lastError) {
      console.error('Error sending message to background:', chrome.runtime.lastError);
      updateIndicator(linkElement, 'error', 'Error');
      return;
    }
  });
} catch (error) {
  console.error('Error sending message to background:', error);
  updateIndicator(linkElement, 'error', 'Error');
}
```

### Background Script Error Handling
```javascript
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // Process message
  if (request.action === 'scanUrl') {
    // Handle async processing
    scanUrl(request.url)
      .then(result => {
        // Send response back
        if (sender.tab && sender.tab.id) {
          chrome.tabs.sendMessage(sender.tab.id, {
            action: 'scanResult',
            url: request.url,
            result: result
          }).catch(error => {
            console.error('Error sending message to content script:', error);
          });
        }
      })
      .catch(error => {
        // Handle errors
      });
    
    // Return true for async response
    return true;
  }
});
```

## 🎯 Success Indicators

When the sendMessage functionality is working properly, you should see:

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

The updated extension handles sendMessage errors gracefully:

1. **Try-Catch Blocks:** Added error handling around sendMessage calls
2. **Callback Error Checking:** Checking `chrome.runtime.lastError` in callbacks
3. **Non-Critical Errors:** Errors are logged but don't break the extension
4. **User Feedback:** Clear visual indicators for different states
5. **Detailed Logging:** More specific error messages for debugging

## 📞 Support

If you continue to experience sendMessage issues:

1. Take screenshots of the error messages
2. Include console logs from both background and content scripts
3. Provide details about your environment:
   - Chrome version
   - Operating system
   - Extension version
   - Backend status

4. Try the sendMessage test page: [send_message_test.html](send_message_test.html)
5. Check the manifest file configuration
6. Verify all extension files are present and correctly formatted