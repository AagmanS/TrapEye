import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from pydantic import BaseModel
from typing import Optional

# Add backend to path to import modules
sys.path.append('backend')

from url_features import URLFeatureExtractor
from model_utils import ModelUtils
from demo_data import get_demo_urls

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
    return FileResponse('frontend/index.html')

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict_phishing(request: PredictionRequest):
    try:
        print(f"Analyzing URL: {request.url[:100]}...")
        features = feature_extractor.extract_features(request.url)
        result = model_utils.predict(features)
        print(f"Prediction: {result['label']} (score: {result['score']:.3f})")
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/demo")
async def get_demo_urls_endpoint():
    return {"demo_urls": get_demo_urls()}

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)