# LinkLens for WhatsApp - Summary

## Overview

LinkLens for WhatsApp is a Chrome extension that automatically detects and analyzes links in WhatsApp Web chats for security risks. It integrates with your existing FastAPI backend to provide real-time link analysis.

## Components

### 1. Manifest File (manifest.json)
- Defines extension metadata, permissions, and entry points
- Specifies content scripts, background service worker, and popup
- Sets required permissions for WhatsApp Web and backend API

### 2. Content Script (content.js)
- Runs on WhatsApp Web pages
- Detects links in chat messages using DOM selectors
- Adds visual indicators next to links (safe/risky)
- Manages the floating panel for displaying results
- Communicates with background service worker

### 3. Content Styles (content.css)
- Provides styling for link indicators
- Defines floating panel appearance
- Creates toggle button styling
- Ensures consistent UI with WhatsApp Web

### 4. Background Service Worker (background.js)
- Handles communication with the FastAPI backend
- Caches results to avoid repeated API calls
- Manages storage of analysis results
- Processes messages from content script

### 5. Popup UI (popup.html & popup.js)
- Provides user interface for extension control
- Shows backend connection status
- Allows manual scanning of current chat
- Offers access to extension settings

### 6. Icons
- Visual identity for the extension
- Used in Chrome toolbar and extension management

## Key Features

### Automatic Link Detection
- Continuously monitors WhatsApp Web for new messages
- Identifies links using multiple CSS selectors for compatibility
- Handles dynamic content loading as users scroll

### Real-time Analysis
- Sends URLs to FastAPI backend for analysis
- Displays results immediately next to links
- Uses color-coded indicators for quick assessment

### Caching System
- Stores analysis results locally using Chrome storage
- Prevents repeated API calls for the same URLs
- Automatically expires cached results after 1 hour

### Floating Panel
- Provides overview of all analyzed links
- Shows detailed results in a compact interface
- Toggle visibility with floating button

### Privacy Focused
- Only sends URLs to backend (no message content)
- All processing happens locally
- No external tracking or data collection

## Technical Implementation

### Message Detection
The extension uses multiple CSS selectors to identify messages in WhatsApp Web:
- `[data-testid="msg-container"]`
- `.message-in`
- `.message-out`
- `[class*="message"]`
- `.copyable-text`

### Link Analysis Flow
1. Content script detects new messages
2. Extracts URLs from message links
3. Checks if URL has been analyzed before
4. Sends new URLs to background service worker
5. Background worker calls FastAPI backend
6. Results are cached and sent back to content script
7. Content script displays indicators next to links
8. Floating panel is updated with new results

### API Integration
- Endpoint: `http://127.0.0.1:8002/predict`
- Method: POST
- Request format: `{"url": "https://example.com"}`
- Response format: `{"label": "safe", "score": 0.0, "reasons": [...], "explainability": [...]}`

## Installation and Usage

### Installation
1. Load unpacked extension in Chrome
2. Ensure FastAPI backend is running on port 8002
3. Navigate to WhatsApp Web

### Usage
- Links are automatically analyzed as they appear
- Green indicators = Safe links
- Red indicators = Risky links
- Click floating button to view all analyzed links

## Files Created

```
linklens-whatsapp/
├── manifest.json
├── content.js
├── content.css
├── background.js
├── popup.html
├── popup.js
├── README.md
├── icons/
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── ...
```

## Testing

A test HTML file ([test_linklens.html](test_linklens.html)) is included to verify the extension works with simulated WhatsApp messages.

## Documentation

- [README.md](linklens-whatsapp/README.md) - Main documentation
- [INSTALL_LINKLENS.md](INSTALL_LINKLENS.md) - Installation guide
- This summary file