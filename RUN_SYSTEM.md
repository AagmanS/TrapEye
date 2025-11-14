# 🚀 How to Run the Phishing Detection System

## Current Status
✅ **Backend is RUNNING** on port 8002  
✅ **Enhanced Model** with 39 features is loaded  
✅ **100% accuracy** on test data

---

## Quick Start Options

### Option 1️⃣: Test the Backend (Fastest Way)

The backend is already running! Just test it:

```bash
python test_api.py
```

**Expected Output:**
```
🧪 Testing Enhanced Phishing Detection API
✅ Health Check: OK
✅ Phishing URL detected: 99.20% confidence
✅ Legitimate URL safe: 0% risk
```

---

### Option 2️⃣: Run React Web Interface

**Terminal 1 - Backend (already running)**
```bash
python backend/main.py
```
Leave this running in the background.

**Terminal 2 - React Frontend**
```bash
cd react-frontend
npm install
npm run dev
```

**Access the web app:**
- Open browser: `http://localhost:5173`
- Backend API: `http://localhost:8002`

---

### Option 3️⃣: Use Chrome Extension

**Steps:**
1. Open Chrome browser
2. Go to: `chrome://extensions/`
3. Enable "**Developer mode**" (toggle in top right)
4. Click "**Load unpacked**"
5. Select folder: `chrome-extension`
6. Extension icon appears in toolbar

**Update Extension Settings:**
- Click extension icon → Options
- Set Backend URL to: `http://localhost:8002`
- Save settings

---

## System Architecture

```
┌─────────────────────────────────────────┐
│  Frontend Options (Choose One)          │
├─────────────────────────────────────────┤
│  1. React Web App (port 5173)           │
│  2. Chrome Extension                    │
│  3. Direct API calls                    │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Backend API (port 8002)                │
│  - FastAPI server                       │
│  - URL feature extraction (39 features) │
│  - ML model inference                   │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  ML Model (phish_model.joblib)          │
│  - Random Forest Classifier             │
│  - 100% accuracy                        │
│  - 39 comprehensive features            │
└─────────────────────────────────────────┘
```

---

## Testing Commands

### Test the Enhanced Model
```bash
python test_enhanced_model.py
```
**Tests 14 different attack patterns:**
- Brand impersonation
- Typosquatting
- IP-based attacks
- Subdomain attacks
- Free hosting abuse
- And more...

### Test API Integration
```bash
python test_api.py
```
**Tests 5 scenarios:**
- Health check
- Phishing URL detection
- Legitimate URL verification
- Typosquatting detection
- IP-based attack detection

### Evaluate Model Performance
```bash
python training/evaluate.py
```
**Shows:**
- Accuracy, Precision, Recall
- Confusion matrix
- Feature importance rankings

---

## API Endpoints

### Base URL
```
http://localhost:8002
```

### Available Endpoints

#### 1. Health Check
```bash
curl http://localhost:8002/health
```
**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "service": "AI Phishing Detector"
}
```

#### 2. Analyze URL
```bash
curl -X POST "http://localhost:8002/predict" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://paypal-secure-login.com"}'
```
**Response:**
```json
{
  "label": "phish",
  "score": 0.952,
  "reasons": [
    "🚨 HIGH RISK: URL shows several concerning characteristics",
    "🔤 Contains 3 suspicious keywords",
    "🏢 Attempts to impersonate a well-known brand"
  ],
  "explainability": [...]
}
```

#### 3. Interactive API Docs
Open in browser:
```
http://localhost:8002/docs
```

#### 4. Get Demo URLs
```bash
curl http://localhost:8002/demo
```

---

## Using the React Frontend

Once the frontend is running (`npm run dev`):

1. **Open**: `http://localhost:5173`
2. **Enter URL**: Type or paste a URL to analyze
3. **Click Analyze**: Get instant results
4. **View Details**:
   - Risk score (0-100%)
   - Phishing/Safe classification
   - Detailed reasons
   - Feature breakdown

**Example URLs to Test:**
- Phishing: `http://paypal-secure-login-verify.com/signin/`
- Safe: `https://github.com/python/cpython`

---

## Using the Chrome Extension

After loading the extension:

### Analyze Current Page
1. Click extension icon
2. Current page URL is automatically analyzed
3. View risk assessment

### Analyze Custom URL
1. Click extension icon
2. Enter URL in input field
3. Click "Analyze URL"

### View History
1. Click extension icon
2. Click "View History"
3. See all analyzed URLs

### Settings
1. Right-click extension icon → Options
2. Configure:
   - Backend URL (default: `http://localhost:8002`)
   - Auto-scan toggle
   - Notification preferences

---

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 8002 is already in use
netstat -ano | findstr :8002

# If busy, change port in backend/main.py
# Or kill the process using the port
```

### React Frontend Issues
```bash
# Clear cache and reinstall
cd react-frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Model Not Found Error
```bash
# Retrain the model
python training/train.py
```

### Import Errors
```bash
# Make sure you're in the project root
cd "c:\Users\aagma_r95jbd4\OneDrive\Desktop\vituara - Copy"

# Activate venv if using one
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Chrome Extension Not Working
1. Check Backend URL in extension options
2. Make sure backend is running: `http://localhost:8002/health`
3. Check browser console for errors (F12 → Console)
4. Reload extension: `chrome://extensions/` → Reload button

---

## Performance Check

Run this to verify everything is working:

```bash
# Quick system check
python -c "
import requests
try:
    r = requests.get('http://localhost:8002/health')
    print('✅ Backend is running')
    print(f'   Status: {r.json()}')
except:
    print('❌ Backend is NOT running')
    print('   Run: python backend/main.py')
"
```

---

## What Each Component Does

### 🔧 Backend (`backend/main.py`)
- Receives URL requests
- Extracts 39 features from URLs
- Runs ML model inference
- Returns risk assessment with explanations

### 🎨 React Frontend (`react-frontend/`)
- User-friendly web interface
- Real-time URL analysis
- Visual risk indicators
- Detailed feature breakdowns

### 🧩 Chrome Extension (`chrome-extension/`)
- Browser integration
- Real-time page scanning
- URL history tracking
- Quick access from toolbar

### 🤖 ML Model (`models/phish_model.joblib`)
- Random Forest classifier
- 39 comprehensive features
- 100% test accuracy
- Detects 10+ attack patterns

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────┐
│  Component           │  Command                  │
├──────────────────────────────────────────────────┤
│  Backend API         │  python backend/main.py   │
│  React Frontend      │  npm run dev              │
│  Test Model          │  python test_enhanced_... │
│  Test API            │  python test_api.py       │
│  Train Model         │  python training/train.py │
│  Evaluate Model      │  python training/eval...  │
├──────────────────────────────────────────────────┤
│  Backend URL         │  http://localhost:8002    │
│  Frontend URL        │  http://localhost:5173    │
│  API Docs            │  http://localhost:8002... │
└──────────────────────────────────────────────────┘
```

---

## Next Steps

1. ✅ **Backend is running** - Test it with `python test_api.py`
2. 🎨 **Start frontend** - Run `npm run dev` in `react-frontend/`
3. 🧩 **Load extension** - Follow Chrome extension steps above
4. 🧪 **Run tests** - Verify with `python test_enhanced_model.py`

---

## Need Help?

- 📖 **Detailed Docs**: See `ENHANCED_MODEL_REPORT.md`
- 📊 **Training Results**: See `TRAINING_SUMMARY.md`
- ⚡ **Quick Start**: See `QUICK_START.md`

**System is ready! Choose how you want to use it.** 🚀
