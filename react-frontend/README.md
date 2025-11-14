# AI Phishing Detector - React Frontend

A professional, vibrant React.js frontend for the AI Phishing Detector project with TypeScript, featuring smooth animations and a modern UI.

## Features

- 🎨 **Vibrant UI Design**: Modern gradient backgrounds with smooth animations
- 🚀 **Real-time URL Analysis**: Analyze URLs for phishing and security risks
- 📊 **Detailed Risk Reports**: Comprehensive analysis with feature impact breakdown
- 🇮🇳 **Cybersecurity Information**: Policies and reporting mechanisms for India
- 🎭 **Smooth Transitions**: Framer Motion animations for enhanced user experience
- 📱 **Responsive Design**: Works on all device sizes

## Project Structure

```
react-frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── URLAnalyzer.tsx
│   │   └── CybersecurityInfo.tsx
│   ├── App.tsx
│   ├── App.css
│   └── index.tsx
├── public/
├── package.json
└── tsconfig.json
```

## Technologies Used

- **React.js** with TypeScript
- **Vite** for fast development
- **Framer Motion** for smooth animations
- **React Router** for navigation
- **Axios** for API requests
- **CSS3** with modern features

## Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

4. **Preview production build**:
   ```bash
   npm run preview
   ```

## Components

### 1. URL Analyzer
- Real-time URL phishing detection
- Detailed risk scoring with visual indicators
- Feature impact analysis
- Model confidence metrics
- Demo URLs for testing

### 2. Cybersecurity Information
- Key cybersecurity policies in India
- Reporting mechanisms and authorities
- Best practices for online safety
- Additional resources and links

## API Integration

The frontend connects to the backend API at `http://localhost:8000/predict` for URL analysis.

## Separation from Chrome Extension

This React frontend is completely separate from the Chrome extension:
- Independent codebase in `react-frontend/` directory
- Different technology stack (React vs. vanilla JS)
- Separate build process and deployment
- No shared code or dependencies with the extension
- Can be hosted independently

## Development

The application uses:
- **Vite** for fast hot-module replacement
- **TypeScript** for type safety
- **CSS Modules** for scoped styling
- **Framer Motion** for declarative animations

## Deployment

Build the application:
```bash
npm run build
```

The output will be in the `dist/` directory, ready for deployment to any static hosting service.