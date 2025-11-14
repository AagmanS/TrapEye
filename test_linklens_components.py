#!/usr/bin/env python3
"""
Comprehensive test script for LinkLens for WhatsApp extension components
"""

import subprocess
import sys
import os
import json
import time
import requests
import webbrowser

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
    """Test the backend API with sample URLs"""
    print("\n🔍 Testing backend API...")
    test_urls = [
        "https://google.com",
        "https://github.com",
        "http://suspicious-site.com/login"
    ]
    
    all_passed = True
    for url in test_urls:
        try:
            response = requests.post(
                "http://127.0.0.1:8002/predict",
                json={"url": url},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API test for {url}: {data['label']} (score: {data['score']})")
            else:
                print(f"❌ API test failed for {url} with status code: {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ Error testing API for {url}: {e}")
            all_passed = False
    
    return all_passed

def check_chrome_processes():
    """Check if Chrome is running"""
    print("\n🔍 Checking Chrome processes...")
    try:
        result = subprocess.run(["tasklist"], capture_output=True, text=True)
        if "chrome.exe" in result.stdout:
            print("✅ Chrome is running")
            return True
        else:
            print("⚠️ Chrome is not running (this is OK if you start it manually)")
            return True  # Not a fatal error
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
    print("🧪 LinkLens for WhatsApp - Comprehensive Component Test")
    print("=" * 60)
    
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
    
    print("\n" + "=" * 60)
    print("📋 Component Test Summary:")
    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All component tests passed!")
        print("\n🚀 To test the complete extension:")
        print("1. Open Chrome and go to chrome://extensions")
        print("2. Enable 'Developer mode'")
        print("3. Click 'Load unpacked' and select the 'linklens-whatsapp' folder")
        print("4. Make sure the extension is enabled")
        print("5. Open https://web.whatsapp.com or the comprehensive test page")
        print("6. Links should be automatically analyzed")
        
        # Ask user if they want to open the test page
        open_test = input("\n❓ Do you want to open the comprehensive test page? (y/n): ")
        if open_test.lower() in ['y', 'yes']:
            try:
                test_page = os.path.join(os.path.dirname(__file__), "comprehensive_test.html")
                if os.path.exists(test_page):
                    webbrowser.open(f"file://{test_page}")
                    print("✅ Test page opened in browser")
                else:
                    print("❌ Test page not found")
            except Exception as e:
                print(f"❌ Error opening test page: {e}")
    else:
        print("⚠️ Some component tests failed. Please review the errors above.")
        print("🔧 Common fixes:")
        print("  - Make sure the FastAPI backend is running on port 8002")
        print("  - Check that all extension files are present")
        print("  - Verify the manifest.json file is correctly configured")
        print("  - Ensure Chrome has permission to access file URLs (if testing locally)")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)