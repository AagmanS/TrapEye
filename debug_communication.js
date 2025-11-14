// Debug script for LinkLens communication issues

// Function to test background script communication
async function testBackgroundCommunication() {
  console.log('Testing background script communication...');
  
  try {
    // Send a test message to background script
    const response = await chrome.runtime.sendMessage({
      action: 'testConnection',
      timestamp: Date.now()
    });
    
    console.log('Background script response:', response);
    return true;
  } catch (error) {
    console.error('Error communicating with background script:', error);
    return false;
  }
}

// Function to test tab messaging
async function testTabMessaging() {
  console.log('Testing tab messaging...');
  
  try {
    // Get current tab
    const tabs = await chrome.tabs.query({active: true, currentWindow: true});
    const currentTab = tabs[0];
    
    if (!currentTab || !currentTab.id) {
      console.error('No active tab found');
      return false;
    }
    
    console.log('Current tab:', currentTab);
    
    // Send test message to content script
    await chrome.tabs.sendMessage(currentTab.id, {
      action: 'testMessage',
      message: 'Hello from debug script'
    });
    
    console.log('Test message sent to content script');
    return true;
  } catch (error) {
    console.error('Error sending message to content script:', error);
    return false;
  }
}

// Run tests
console.log('LinkLens Communication Debug Script');
console.log('====================================');

// Test background communication
testBackgroundCommunication().then(result => {
  console.log('Background communication test:', result ? 'PASSED' : 'FAILED');
});

// Test tab messaging (this will only work in a content script context)
// testTabMessaging().then(result => {
//   console.log('Tab messaging test:', result ? 'PASSED' : 'FAILED');
// });

// Add listener for test messages
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Received message in debug script:', request);
  
  if (request.action === 'testResponse') {
    console.log('Test response received:', request.data);
  }
  
  // Send response back
  if (request.action === 'testConnection') {
    sendResponse({
      status: 'connected',
      timestamp: Date.now(),
      message: 'Debug script is running'
    });
  }
});