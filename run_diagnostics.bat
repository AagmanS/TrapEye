@echo off
title LinkLens Communication Diagnostics

echo =====================================================
echo      LinkLens for WhatsApp - Communication Diagnostics
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
echo 🚀 Diagnostic Summary:
echo    - Check Chrome extensions page (chrome://extensions)
echo    - Ensure LinkLens is enabled and loaded
echo    - Verify permissions for web.whatsapp.com
echo    - Check console logs for detailed error information
echo.
echo 📖 For detailed troubleshooting, see: communication_troubleshooting.md
echo.
echo 💡 Tips:
echo    1. Refresh WhatsApp Web after loading the extension
echo    2. Check that you're on https://web.whatsapp.com
echo    3. Look for "LinkLens for WhatsApp content script loaded" in console
echo    4. Test with communication_test.html
echo.
pause