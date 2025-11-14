from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add the current directory to Python path to find local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Now import local modules
try:
    from url_features import URLFeatureExtractor
    from model_utils import ModelUtils
    from demo_data import get_demo_urls
    print("✅ All backend modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Current directory:", current_dir)
    print("Files in backend directory:", os.listdir(current_dir))
    raise

# ✅ Make sure this line exists and the variable is named 'app'
app = FastAPI(
    title="AI Phishing Detector API",
    description="Defensive ML system for detecting malicious URLs",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
print("Initializing feature extractor and model...")
feature_extractor = URLFeatureExtractor()
model_utils = ModelUtils()

class PredictionRequest(BaseModel):
    url: str
    message: Optional[str] = ""

class PredictionResponse(BaseModel):
    label: str
    score: float
    reasons: list
    explainability: list

@app.get("/")
async def serve_frontend():
    """Serve the main frontend"""
    frontend_path = os.path.join(os.path.dirname(current_dir), 'frontend', 'index.html')
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {"error": "Frontend not found", "path": frontend_path}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "model_loaded": model_utils.model is not None,
        "service": "AI Phishing Detector"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_phishing(request: PredictionRequest):
    """Analyze URL for phishing probability"""
    try:
        print(f"Analyzing URL: {request.url[:100]}...")
        
        # Extract features from URL
        features = feature_extractor.extract_features(request.url)
        
        # Make prediction
        result = model_utils.predict(features)
        
        print(f"Prediction: {result['label']} (score: {result['score']:.3f})")
        return PredictionResponse(**result)
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/demo")
async def get_demo_urls_endpoint():
    """Get curated demo URLs for testing"""
    return {"demo_urls": get_demo_urls()}

# FIXED: Mount static files with correct path
project_root = os.path.dirname(current_dir)  # Go up one level from backend/
frontend_static_path = os.path.join(project_root, 'frontend', 'static')
frontend_templates_path = os.path.join(project_root, 'frontend', 'templates')

print(f"🔍 Project root: {project_root}")
print(f"📁 Static path: {frontend_static_path}")
print(f"📁 Templates path: {frontend_templates_path}")

# Check if directories exist
if os.path.exists(frontend_static_path):
    app.mount("/static", StaticFiles(directory=frontend_static_path), name="static")
    print(f"✅ Static files mounted from: {frontend_static_path}")
else:
    print(f"❌ Static directory not found: {frontend_static_path}")

if os.path.exists(frontend_templates_path):
    print(f"✅ Templates directory found: {frontend_templates_path}")
else:
    print(f"❌ Templates directory not found: {frontend_templates_path}")

if __name__ == "__main__":
    print("\n🚀 Starting FastAPI server...")
    print("📡 API Documentation: http://localhost:8002/docs")
    print("🌐 Health Check: http://localhost:8002/health")
    print("\n" + "="*50)
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=False)