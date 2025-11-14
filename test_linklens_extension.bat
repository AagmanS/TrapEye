@echo off
title LinkLens for WhatsApp - Extension Test

echo ======================================================
echo        LinkLens for WhatsApp - Extension Test        
echo ======================================================
echo.

echo 🧪 Running comprehensive component tests...
echo.

python test_linklens_components.py

echo.
echo ======================================================
echo                    Test Complete                     
echo ======================================================
echo.
echo 🚀 Next steps:
echo 1. Load the extension in Chrome (chrome://extensions)
echo 2. Open WhatsApp Web (https://web.whatsapp.com)
echo 3. Test with the comprehensive test page
echo.
echo 📋 For detailed instructions, see final_verification.md
echo.
echo 🔧 If you encounter issues:
echo    - Check that the FastAPI backend is running on port 8002
echo    - Verify all extension files are present
echo    - Ensure Chrome has proper permissions
echo.
pause