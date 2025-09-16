# AI Wallpaper Generator

A powerful AI-powered wallpaper generator built with FastAPI backend and HTML/CSS/JavaScript frontend. Uses Stable Diffusion LCM (Latent Consistency Model) for fast, high-quality wallpaper generation.

## Features

- 🎨 Multiple artistic styles (Gradient, Geometric, Organic, Vibrant, Minimal, Fractal, Crystal, Retro Wave, Botanical, Space Cosmic, Psychedelic, Industrial)
- 📐 Multiple resolutions (Mobile Portrait, Desktop, Square, Ultrawide, 4K)
- 🎲 Random seed generation and seed copying
- 🎪 Color palette extraction from generated images
- ⚡ Fast generation using LCM (Latent Consistency Model)
- 🔧 No Docker required - runs locally with Python
- 💾 Smart model caching (converts from safetensors to .bin for faster loading)

## Project Structure

```
warpw/
├── backend/
│   ├── main.py              # FastAPI server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html          # Web interface
│   ├── script.js           # Frontend logic
│   └── style.css           # Styling
├── models/                 # Model storage (auto-created)
├── .venv/                  # Python virtual environment
├── start_server.ps1        # PowerShell startup script
└── README.md              # This file
```

## Quick Start

1. **Run the application:**
   ```powershell
   .\start_server.ps1
   ```

2. **Access the web interface:**
   - Open your browser to: `http://127.0.0.1:8080`

3. **Generate wallpapers:**
   - Choose a style, adjust settings, and click "Generate"
   - The first run will download and convert the AI model (one-time process)

## Manual Setup

If you prefer to run components separately:

### Backend (API Server)
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the FastAPI server
python backend\main.py
```
Server will be available at: `http://127.0.0.1:8000`

### Frontend (Web Interface)
```powershell
# In another terminal, serve the frontend
cd frontend
python -m http.server 8080
```
Web interface will be available at: `http://127.0.0.1:8080`

## Model Information

- **Model:** SimianLuo/LCM_Dreamshaper_v7
- **Type:** Latent Consistency Model (LCM) for Stable Diffusion
- **Benefits:** Fast generation (4 steps instead of 50+)
- **Storage:** Models are automatically cached locally and converted from safetensors to .bin format for optimal performance

### Model Conversion Process

On first run, the application will:
1. Detect existing safetensors model files
2. Convert them to .bin format for faster loading
3. Save the converted model to `models/SimianLuo_LCM_Dreamshaper_v7_bin/`
4. Use the .bin version for all subsequent runs (no re-downloading)

## API Endpoints

- `POST /generate-wallpaper/` - Generate a wallpaper
- `GET /random-seed/` - Get a random seed
- `GET /health` - Health check

## System Requirements

- **Python:** 3.8+
- **RAM:** 8GB+ recommended
- **Storage:** 5GB+ for models
- **GPU:** Optional (CUDA supported, but runs on CPU)

## Stopping the Application

Press `Ctrl+C` in the terminal to stop both servers.

## Troubleshooting

### Models Not Loading
- Ensure you have sufficient disk space (5GB+)
- Check internet connection for initial model download
- Models are cached in the `models/` directory

### Performance Issues
- For faster generation, use a CUDA-compatible GPU
- Reduce image resolution if generation is slow
- Close other memory-intensive applications

### Port Conflicts
- Backend runs on port 8000
- Frontend runs on port 8080
- Change ports in the respective configuration files if needed

## Technical Notes

- **No Docker dependency** - Runs natively with Python
- **Smart caching** - Models downloaded once, converted to optimal format
- **Cross-platform** - Works on Windows (PowerShell scripts provided)
- **Extensible** - Easy to add new styles and features
