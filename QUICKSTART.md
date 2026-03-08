# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites
- Python 3.8+
- Webcam or video file
- 2GB free disk space

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/object-tracking.git
cd object-tracking
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

The first run will automatically download the YOLOv8 model (~30 seconds).

## Run Tracker

### Using Webcam
```bash
python tracker.py
```

### Using Video File
Edit `config.py`:
```python
VIDEO_SOURCE = "path/to/your/video.mp4"
```

Then run:
```bash
python tracker.py
```

## Controls

| Key | Action |
|-----|--------|
| **s** | Select object to track |
| **r** | Reset and re-select |
| **q** | Quit |

## Configuration

Customize behavior in `config.py`:

```python
# Faster tracking (less accurate)
YOLO_MODEL = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.6

# More accurate tracking (slower)
YOLO_MODEL = "yolov8l.pt"
CONFIDENCE_THRESHOLD = 0.4

# Better tracking persistence
DEEPSORT_MAX_AGE = 50  # Keep track 50 frames

# Larger video
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
```

## Common Issues

**Q: Program runs slow**  
A: Reduce video resolution in `config.py`

**Q: Webcam not found**  
A: Try `VIDEO_SOURCE = 1` in config.py

**Q: Tracking ID changes frequently**  
A: Increase `DEEPSORT_MAX_AGE` in config.py

**Q: Model download fails**  
A: Run `python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"`

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Open an issue for support

## Performance Benchmark

On Intel i7 with RTX 3060:
- **YOLOv8n**: ~150 FPS
- **YOLOv8s**: ~100 FPS  
- **YOLOv8m**: ~60 FPS

FPS varies by resolution, video content, and hardware.

---

Enjoy tracking! 🎯
