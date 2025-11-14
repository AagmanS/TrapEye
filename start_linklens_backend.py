#!/usr/bin/env python3
"""
Script to start the LinkLens backend server
"""

import subprocess
import sys
import os

def start_backend():
    """Start the FastAPI backend server for LinkLens"""
    print("🚀 Starting LinkLens Backend Server...")
    print("📝 This script will start the FastAPI server on port 8002")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        if not os.path.exists(backend_dir):
            print(f"❌ Backend directory not found: {backend_dir}")
            return False
            
        # Start the server
        print("🔄 Starting server...")
        process = subprocess.Popen([
            sys.executable, 
            'main.py'
        ], cwd=backend_dir)
        
        print("✅ Server started successfully!")
        print("🌐 Access the API at: http://127.0.0.1:8002")
        print("📄 API Documentation: http://127.0.0.1:8002/docs")
        print("❤️  Health Check: http://127.0.0.1:8002/health")
        print("\n⏳ Server is running... Press Ctrl+C to stop")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
        print("✅ Server stopped")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    start_backend()