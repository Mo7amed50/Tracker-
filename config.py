"""
Configuration file for Object Tracking System
"""

# Model Configuration
YOLO_MODEL = "yolov8n.pt"  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
CONFIDENCE_THRESHOLD = 0.5

# DeepSORT Configuration
DEEPSORT_MAX_AGE = 30  # Maximum frames to keep alive a track without detections
DEEPSORT_N_INIT = 3  # Number of frames to be considered as unconfirmed track

# Video Configuration
VIDEO_SOURCE = 0  # 0 for webcam, or path to video file
VIDEO_WIDTH = 960
VIDEO_HEIGHT = 540
TARGET_FPS = 30

# Display Configuration
SHOW_FPS = True
SHOW_CONFIDENCE = True
BBOX_COLOR = (0, 255, 0)  # BGR format
BBOX_THICKNESS = 3
TEXT_COLOR = (0, 0, 0)
TEXT_FONT_SIZE = 0.6
LABEL_BG_COLOR = (0, 255, 0)

# Tracking Configuration
ENABLE_ROI_SELECTION = True  # Allow user to select Region of Interest
TRACK_SPECIFIC_OBJECT = True  # Track only the selected object or all objects

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
ENABLE_FILE_LOGGING = False
LOG_FILE = "tracking.log"
