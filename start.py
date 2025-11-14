import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Start the server without changing directory
    uvicorn.run(
        "backend.main:app", 
        host="0.0.0.0", 
        port=8002,  # Changed from 8000 to 8002 to match backend configuration
        reload=True,
        reload_dirs=[str(project_root)]  # Specify what directories to watch
    )