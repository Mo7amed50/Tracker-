# Object Tracking System - YOLOv8 + DeepSORT

A real-time multi-object tracking system that combines YOLOv8 object detection with DeepSORT algorithm for robust and persistent tracking across video frames. The system displays live tracking results in a video feed with unique object IDs.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

- **Real-time Object Detection**: YOLOv8 nano model for fast detection
- **Multi-Object Tracking**: Persistent tracking across frames using DeepSORT
- **Live Video Feed**: Display tracking results with bounding boxes and object IDs
- **Interactive ROI Selection**: Select specific objects to track
- **FPS Display**: Real-time performance monitoring
- **Configurable Settings**: Easy configuration through `config.py`
- **Logging Support**: Comprehensive logging for debugging

## 📋 Implementation Details

### Architecture

The system uses a two-stage approach:

1. **Detection Stage (YOLOv8)**
   - Detects objects in each frame using YOLOv8 model
   - Outputs bounding boxes and class predictions
   - Confidence threshold filtering for quality detections

2. **Tracking Stage (DeepSORT)**
   - Maintains object identities across frames
   - Uses appearance features and motion estimation
   - Handles occlusions and temporary detections loss
   - Assigns unique IDs to tracked objects

### Key Components

**`tracker.py`** - Main tracking engine
- `ObjectTracker` class: Manages detection and tracking lifecycle
- Methods for object detection, track updates, and visualization
- FPS monitoring and performance metrics

**`config.py`** - Configuration management
- Model selection and parameters
- Video input/output settings
- Display customization options
- DeepSORT parameters

### How It Works

```
Input Frame
    ↓
[Detection] → YOLOv8 extracts bounding boxes
    ↓
[Tracking] → DeepSORT associates detections with existing tracks
    ↓
[Display] → Annotate frame with IDs, confidence, class labels
    ↓
Output Frame with Tracking Results
```

### Algorithm Details

- **YOLOv8**: Ultrafast real-time object detection
- **DeepSORT**: Incorporates appearance and motion cues for tracking
- **Kalman Filter**: Predicts object motion and handles missing detections
- **Hungarian Algorithm**: Optimal assignment between detections and tracks

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam or video file
- Windows/macOS/Linux

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/object-tracking.git
cd object-tracking
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download YOLO Model
The YOLOv8 model will be automatically downloaded on first run. Alternatively, download manually:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## 📹 Usage

### Run with Webcam
```bash
python tracker.py
```

### Run with Video File
Edit `config.py`:
```python
VIDEO_SOURCE = "path/to/video.mp4"  # Instead of 0
```

Then run:
```bash
python tracker.py
```

### Controls
- **Press 's'**: Select object to track (draws ROI selection box)
- **Press 'r'**: Reset tracking and re-select object
- **Press 'q'**: Quit application

## ⚙️ Configuration

Modify `config.py` to customize:

```python
# Model Configuration
YOLO_MODEL = "yolov8n.pt"  # yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
CONFIDENCE_THRESHOLD = 0.5

# Video Configuration
VIDEO_WIDTH = 960
VIDEO_HEIGHT = 540
TARGET_FPS = 30

# Tracking
DEEPSORT_MAX_AGE = 30  # Frames to keep track alive
DEEPSORT_N_INIT = 3    # Frames until track confirmed

# Display
SHOW_FPS = True
BBOX_COLOR = (0, 255, 0)  # BGR format
TEXT_FONT_SIZE = 0.6
```

## 📊 Model Sizes & Performance

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| YOLOv8n | 3.2MB | ⚡⚡⚡ Fast | Good | Real-time, Edge devices |
| YOLOv8s | 11MB | ⚡⚡ Medium | Better | Balanced |
| YOLOv8m | 26MB | ⚡ Slower | Best | High accuracy needed |
| YOLOv8l | 52MB | Slowest | Very High | Maximum accuracy |

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| ultralytics | ≥8.0.0 | YOLOv8 object detection |
| opencv-python | ≥4.8.0 | Video capture & drawing |
| deep-sort-realtime | Latest | Multi-object tracking |
| numpy | ≥1.24.0 | Numerical operations |
| scipy | ≥1.10.0 | Hungarian algorithm |
| filterpy | ≥1.4.5 | Kalman filter |

## 🎓 System Requirements

**Minimum:**
- CPU: Intel i5 or equivalent
- RAM: 4GB
- Storage: 5GB (for models)

**Recommended:**
- CPU: Intel i7+ or AMD Ryzen 5+
- RAM: 8GB+
- GPU: NVIDIA GPU with CUDA support (for faster inference)
- Storage: 10GB

## 📈 Performance Tips

1. **Use Smaller Model**: `yolov8n` is optimized for speed
2. **Lower Resolution**: Reduce `VIDEO_WIDTH` and `VIDEO_HEIGHT` in config
3. **Increase Confidence Threshold**: Skip weak detections with higher `CONFIDENCE_THRESHOLD`
4. **GPU Acceleration**: Install CUDA for GPU inference (10x+ faster)
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

## 🐛 Troubleshooting

### Issue: Slow Performance
- Use smaller video resolution
- Use smaller model (yolov8n)
- Increase confidence threshold
- Ensure GPU drivers are updated

### Issue: Tracking Lost / Object ID Changes Frequently
- Increase `DEEPSORT_MAX_AGE` for longer track persistence
- Lower `CONFIDENCE_THRESHOLD` for more detections
- Improve lighting conditions

### Issue: Model Download Fails
```bash
# Force model download
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Issue: Webcam Not Found
```bash
# Try different camera index
VIDEO_SOURCE = 1  # Instead of 0
```

## 🎥 Recording a Demo

### Option 1: Screen Recording Software
- **Windows**: Use built-in Game Bar (Win + G)
- **macOS**: Use QuickTime Player
- **Linux**: Use OBS Studio

### Option 2: Modify Code to Save Video
Add to `tracker.py` after opening video:
```python
# Add after opening cap
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('demo_output.mp4', fourcc, 30.0, (VIDEO_WIDTH, VIDEO_HEIGHT))

# In main loop, after imshow:
out.write(frame)

# At cleanup:
out.release()
```

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- **Ultralytics** - YOLOv8 implementation
- **DeepSORT** - Multi-object tracking algorithm
- **OpenCV** - Computer vision library

---

**Last Updated**: March 2026  
**Version**: 1.0.0
