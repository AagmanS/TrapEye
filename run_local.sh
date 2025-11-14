#!/bin/bash

echo "=== AI Phishing Detector Setup ==="

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate  # Linux/Mac
else
    source venv/Scripts/activate  # Windows
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p models frontend/static tools/fake_login_demo

# Train the model (skip if flag set)
if [ "$SKIP_TRAIN" = "1" ]; then
    echo "Skipping model training..."
else
    echo "Training model..."
    python training/train.py
fi

# Start the server
echo "Starting FastAPI server..."
echo "Open http://localhost:8000 in your browser"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload