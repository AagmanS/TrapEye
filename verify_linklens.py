#!/usr/bin/env python3
"""
Verification script for LinkLens for WhatsApp extension
"""

import subprocess
import sys
import os
import json
import time
import requests

def check_backend():
    """Check if the FastAPI backend is running"""
    print("🔍 Checking FastAPI backend...")
    try:
        response = requests.get("http://127.0.0.1:8002/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running: {data}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running or not accessible on port 8002")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def test_backend_api():
    """Test the backend API with a sample URL"""
    print("\n🔍 Testing backend API...")
    try:
        response = requests.post(
            "http://127.0.0.1:8002/predict",
            json={"url": "https://google.com"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API test successful: {data}")
            return True
        else:
            print(f"❌ API test failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def check_chrome_processes():
    """Check if Chrome is running"""
    print("\n🔍 Checking Chrome processes...")
    try:
        result = subprocess.run(["tasklist"], capture_output=True, text=True)
        if "chrome.exe" in result.stdout:
            print("✅ Chrome is running")
            return True
        else:
            print("❌ Chrome is not running")
            return False
    except Exception as e:
        print(f"❌ Error checking Chrome processes: {e}")
        return False

def verify_extension_files():
    """Verify that all extension files exist"""
    print("\n🔍 Verifying extension files...")
    extension_dir = os.path.join(os.path.dirname(__file__), "linklens-whatsapp")
    required_files = [
        "manifest.json",
        "content.js",
        "content.css",
        "background.js",
        "popup.html",
        "popup.js"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(extension_dir, file)
        if os.path.exists(file_path):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_manifest():
    """Check manifest file for common issues"""
    print("\n🔍 Checking manifest file...")
    manifest_path = os.path.join(os.path.dirname(__file__), "linklens-whatsapp", "manifest.json")
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        # Check required fields
        required_fields = ["manifest_version", "name", "version"]
        missing_fields = [field for field in required_fields if field not in manifest]
        if missing_fields:
            print(f"❌ Missing fields in manifest: {', '.join(missing_fields)}")
            return False
        
        # Check content scripts
        if "content_scripts" not in manifest:
            print("❌ No content_scripts defined")
            return False
        
        # Check permissions
        if "host_permissions" not in manifest:
            print("❌ No host_permissions defined")
            return False
        
        host_permissions = manifest.get("host_permissions", [])
        required_permissions = ["http://127.0.0.1:8002/*", "https://web.whatsapp.com/*"]
        missing_permissions = [perm for perm in required_permissions if perm not in host_permissions]
        if missing_permissions:
            print(f"❌ Missing host permissions: {', '.join(missing_permissions)}")
            return False
        
        print("✅ Manifest file looks good")
        return True
    except Exception as e:
        print(f"❌ Error reading manifest file: {e}")
        return False

def main():
    """Main verification function"""
    print("🧪 LinkLens for WhatsApp - Verification Script")
    print("=" * 50)
    
    checks = [
        ("Backend Status", check_backend),
        ("API Test", test_backend_api),
        ("Chrome Processes", check_chrome_processes),
        ("Extension Files", verify_extension_files),
        ("Manifest File", check_manifest)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} failed with error: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 50)
    print("📋 Verification Summary:")
    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! LinkLens should be working correctly.")
        print("\nTo test the extension:")
        print("1. Open Chrome and go to chrome://extensions")
        print("2. Make sure LinkLens is enabled")
        print("3. Open https://web.whatsapp.com")
        print("4. Scan a QR code to log in")
        print("5. Open a chat with links")
        print("6. Links should be automatically analyzed")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print("Refer to TROUBLESHOOTING_LINKLENS.md for detailed solutions.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)