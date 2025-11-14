@echo off
title LinkLens sendMessage Diagnostics

echo =====================================================
echo      LinkLens for WhatsApp - sendMessage Diagnostics
echo =====================================================
echo.

echo 🧪 Testing backend connectivity...
echo.

curl -Method GET -Uri "http://127.0.0.1:8002/health" -TimeoutSec 5 >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Backend is running on port 8002
) else (
    echo ❌ Backend is not accessible on port 8002
    echo    Please start the FastAPI backend with: python backend/main.py
)

echo.
echo 🔍 Checking Chrome processes...
echo.

tasklist | findstr chrome >nul
if %errorlevel% == 0 (
    echo ✅ Chrome is running
) else (
    echo ⚠️ Chrome is not running
)

echo.
echo 📁 Verifying extension files...
echo.

if exist "linklens-whatsapp\manifest.json" (
    echo ✅ manifest.json found
) else (
    echo ❌ manifest.json missing
)

if exist "linklens-whatsapp\content.js" (
    echo ✅ content.js found
) else (
    echo ❌ content.js missing
)

if exist "linklens-whatsapp\background.js" (
    echo ✅ background.js found
) else (
    echo ❌ background.js missing
)

echo.
echo 📋 sendMessage Test Checklist:
echo    1. Extension loaded and enabled in chrome://extensions
echo    2. Background script running (check Inspect views)
echo    3. Content script loaded (check WhatsApp Web console)
echo    4. Proper message format being sent
echo    5. Correct tab context for messaging
echo.
echo 🚀 Diagnostic Summary:
echo    - Check Chrome extensions page (chrome://extensions)
echo    - Ensure LinkLens is enabled and loaded
echo    - Verify permissions for web.whatsapp.com
echo    - Check console logs for detailed error information
echo.
echo 📖 For detailed troubleshooting, see: send_message_troubleshooting.md
echo.
echo 💡 Tips:
echo    1. Refresh WhatsApp Web after loading the extension
echo    2. Check that you're on https://web.whatsapp.com
echo    3. Look for "LinkLens for WhatsApp content script loaded" in console
echo    4. Test with send_message_test.html
echo    5. Check background script console for "background service started"
echo.
pause