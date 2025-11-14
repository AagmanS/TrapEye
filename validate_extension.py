import json
import os

def validate_chrome_extension():
    """Validate the Chrome extension structure and manifest"""
    
    extension_path = "chrome-extension"
    
    # Check if extension directory exists
    if not os.path.exists(extension_path):
        print("❌ Error: chrome-extension directory not found")
        return False
    
    # Check manifest file
    manifest_path = os.path.join(extension_path, "manifest.json")
    if not os.path.exists(manifest_path):
        print("❌ Error: manifest.json not found")
        return False
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in manifest.json: {e}")
        return False
    
    # Validate required manifest fields
    required_fields = ["manifest_version", "name", "version"]
    for field in required_fields:
        if field not in manifest:
            print(f"❌ Error: Missing required field '{field}' in manifest.json")
            return False
    
    # Check manifest version
    if manifest["manifest_version"] != 3:
        print("❌ Error: Manifest version must be 3")
        return False
    
    # Check background script
    if "background" in manifest and "service_worker" in manifest["background"]:
        bg_script = os.path.join(extension_path, manifest["background"]["service_worker"])
        if not os.path.exists(bg_script):
            print(f"❌ Error: Background script '{manifest['background']['service_worker']}' not found")
            return False
    
    # Check content scripts
    if "content_scripts" in manifest:
        for i, script in enumerate(manifest["content_scripts"]):
            if "js" in script:
                for js_file in script["js"]:
                    js_path = os.path.join(extension_path, js_file)
                    if not os.path.exists(js_path):
                        print(f"❌ Error: Content script '{js_file}' not found")
                        return False
    
    # Check action popup
    if "action" in manifest and "default_popup" in manifest["action"]:
        popup_path = os.path.join(extension_path, manifest["action"]["default_popup"])
        if not os.path.exists(popup_path):
            print(f"❌ Error: Popup file '{manifest['action']['default_popup']}' not found")
            return False
    
    # Check options page
    if "options_page" in manifest:
        options_path = os.path.join(extension_path, manifest["options_page"])
        if not os.path.exists(options_path):
            print(f"❌ Error: Options page '{manifest['options_page']}' not found")
            return False
    
    # Check icons
    if "icons" in manifest:
        for size, icon_path in manifest["icons"].items():
            full_icon_path = os.path.join(extension_path, icon_path)
            if not os.path.exists(full_icon_path):
                print(f"❌ Error: Icon file '{icon_path}' not found")
                return False
    
    print("✅ Chrome extension structure validation passed!")
    print(f"   Name: {manifest.get('name', 'N/A')}")
    print(f"   Version: {manifest.get('version', 'N/A')}")
    print(f"   Description: {manifest.get('description', 'N/A')}")
    
    return True

if __name__ == "__main__":
    validate_chrome_extension()