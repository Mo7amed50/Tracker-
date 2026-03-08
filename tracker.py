"""
Multi-Object Tracking System using YOLOv8 and DeepSORT
Displays live tracking results in video feed with object IDs
"""

import cv2
import time
import logging
import threading
from deep_sort_realtime.deepsort_tracker import DeepSort
from config import *

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ObjectTracker:
    """Multi-Object Tracker using YOLOv8 + DeepSORT"""
    
    def __init__(self, model_name=YOLO_MODEL, confidence=CONFIDENCE_THRESHOLD):
        """
        Initialize tracker with YOLO model and DeepSORT
        
        Args:
            model_name (str): YOLOv8 model name
            confidence (float): Detection confidence threshold
        """
        logger.info(f"Initializing ObjectTracker with model: {model_name}")
        
        # Lazy load YOLO to avoid slow import at startup
        self.model = None
        self.model_name = model_name
        self.confidence = confidence
        self.class_names = None
        
        # Load YOLO model with timeout
        self._load_yolo_model()
        
        # Initialize DeepSORT
        self._load_deepsort()
        
        # Check GUI availability
        self.gui_available = self._check_gui_available()
        
        logger.info("ObjectTracker initialized successfully")
        self.selected_track_id = None
        self.roi = None
        self.roi_center = None
        self.fps = 0
        self.fps_time = time.time()
        
        logger.info("ObjectTracker initialized successfully")
    
    def _load_yolo_model(self):
        """Load YOLO model with progress indication and timeout"""
        logger.info(f"Loading YOLO model: {self.model_name} (this may take 30-60 seconds on first run)")
        
        # Use threading to load with timeout
        result = [None]
        exception = [None]
        
        def load_model():
            try:
                logger.info("Importing ultralytics (this is the slow part)...")
                from ultralytics import YOLO
                logger.info("Creating YOLO model...")
                result[0] = YOLO(self.model_name)
                logger.info("YOLO model loaded successfully")
            except Exception as e:
                exception[0] = e
        
        # Start loading in background
        load_thread = threading.Thread(target=load_model, daemon=True)
        load_thread.start()
        
        # Wait with progress indication
        start_time = time.time()
        timeout = 30  # 30 seconds timeout
        
        while load_thread.is_alive() and (time.time() - start_time) < timeout:
            elapsed = time.time() - start_time
            if elapsed > 5:  # Show progress after 5 seconds
                logger.info(f"Loading YOLO model... ({int(elapsed)}s elapsed)")
            time.sleep(1)  # Check every 1 second
        
        load_thread.join(timeout=1)  # Give it 1 more second
        
        if load_thread.is_alive():
            raise TimeoutError(f"YOLO model loading timed out after {timeout} seconds. "
                             "Try restarting or check your internet connection for model download.")
        
        if exception[0]:
            raise exception[0]
        
        self.model = result[0]
        self.class_names = self.model.names
        logger.info(f"YOLO model ready with {len(self.class_names)} classes")
    
    def _load_deepsort(self):
        """Initialize DeepSORT tracker"""
        logger.info("Initializing DeepSORT tracker")
        self.tracker = DeepSort(max_age=DEEPSORT_MAX_AGE, n_init=DEEPSORT_N_INIT)
        logger.info("DeepSORT tracker initialized")
    
    def _check_gui_available(self):
        """Check if GUI display is available"""
        # force GUI
        return True
    
    def detect_objects(self, frame):
        """
        Detect objects in frame using YOLOv8
        
        Args:
            frame: Input frame
            
        Returns:
            list: Detections in format [(bbox, conf, cls), ...]
        """
        results = self.model(frame, conf=self.confidence)[0]
        detections = []
        
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            
            # Convert to [x, y, w, h] format for DeepSORT
            detections.append(([x1, y1, x2-x1, y2-y1], conf, cls))
        
        logger.debug(f"Detected {len(detections)} objects")
        return detections
    
    def update_tracks(self, detections, frame):
        """
        Update tracks with new detections
        
        Args:
            detections: List of detections
            frame: Current frame
            
        Returns:
            list: Updated tracks
        """
        tracks = self.tracker.update_tracks(detections, frame=frame)
        return tracks
    
    def select_roi(self, frame):
        """
        Allow user to select Region of Interest
        
        Args:
            frame: Current frame
            
        Returns:
            tuple: ROI coordinates (x, y, w, h)
        """
        roi = cv2.selectROI("Object Tracking - Select Object", frame, False)
        logger.info(f"ROI selected: {roi}")
        return roi
    
    def draw_detections(self, frame, tracks):
        """
        Draw tracking results on frame
        
        Args:
            frame: Input frame
            tracks: List of tracked objects
            
        Returns:
            frame: Annotated frame
        """
        for track in tracks:
            if not track.is_confirmed():
                continue
            
            track_id = track.track_id
            l, t, r, b = track.to_ltrb()
            
            cx = (l + r) / 2
            cy = (t + b) / 2
            
            # Select specific object if ROI is set
            if self.selected_track_id is None and self.roi_center is not None:
                rx, ry, rw, rh = self.roi
                if abs(cx - self.roi_center[0]) < rw and abs(cy - self.roi_center[1]) < rh:
                    self.selected_track_id = track_id
                    logger.info(f"Selected object: Track ID {track_id}")
            
            # Draw only selected object or all objects
            if self.selected_track_id is None or track_id == self.selected_track_id:
                x1, y1, x2, y2 = int(l), int(t), int(r), int(b)
                
                # Get class name
                cls_id = track.det_class
                label = self.class_names.get(cls_id, "Object") if cls_id is not None else "Object"
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), BBOX_COLOR, BBOX_THICKNESS)
                
                # Draw label background
                cv2.rectangle(frame, (x1, y1-30), (x1+220, y1), LABEL_BG_COLOR, -1)
                
                # Draw label text
                text = f"{label} | ID:{track_id}"
                if SHOW_CONFIDENCE:
                    conf = getattr(track, 'det_conf', None)
                    if conf is not None:
                        text += f" | {conf:.2f}"
                    else:
                        text += " | N/A"
                
                cv2.putText(frame, text, (x1+5, y1-8),
                           cv2.FONT_HERSHEY_SIMPLEX, TEXT_FONT_SIZE,
                           TEXT_COLOR, 2)
        
        return frame
    
    def draw_info(self, frame):
        """
        Draw FPS and instructions on frame
        
        Args:
            frame: Input frame
            
        Returns:
            frame: Annotated frame
        """
        # Draw FPS
        if SHOW_FPS:
            cv2.putText(frame, f"FPS: {int(self.fps)}",
                       (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                       0.8, (255, 255, 0), 2)
        
        # Draw instructions if ROI not selected
        if self.roi is None:
            cv2.putText(frame, "Press 's' to select object | 'q' to quit",
                       (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                       0.8, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Tracking active | 'r' to reset | 'q' to quit",
                       (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                       0.8, (0, 255, 0), 2)
        
        return frame
    
    def update_fps(self):
        """Update FPS counter"""
        new_time = time.time()
        self.fps = 1 / (new_time - self.fps_time) if (new_time - self.fps_time) > 0 else 0
        self.fps_time = new_time


def main():
    """Main tracking loop"""
    logger.info("Starting Object Tracker")
    
    # Initialize tracker
    tracker = ObjectTracker()
    
    # Open video source
    logger.info(f"Opening video source: {VIDEO_SOURCE}")
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    
    if not cap.isOpened():
        logger.error("Failed to open video source")
        return
    
    # Set video properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
    
    logger.info("Tracker ready. Starting main loop...")
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            logger.warning("Failed to read frame")
            break
        
        frame_count += 1
        
        # Resize frame
        frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
        
        # ROI Selection Mode
        if tracker.roi is None:
            if tracker.gui_available:
                cv2.imshow("Object Tracking", tracker.draw_info(frame))
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('s'):
                    tracker.roi = tracker.select_roi(frame)
                    rx, ry, rw, rh = tracker.roi
                    tracker.roi_center = (rx + rw/2, ry + rh/2)
                elif key == ord('q'):
                    logger.info("Quit command received")
                    break
            else:
                # No GUI - auto-select first detected object
                logger.info("No GUI available. Auto-selecting first detected object...")
                detections = tracker.detect_objects(frame)
                if detections:
                    # Select first detection as ROI
                    x1, y1, w, h = detections[0][0]
                    cx, cy = x1 + w/2, y1 + h/2
                    tracker.roi = (x1, y1, w, h)
                    tracker.roi_center = (cx, cy)
                    logger.info(f"Auto-selected object at center ({cx:.1f}, {cy:.1f})")
                else:
                    logger.info("No objects detected, continuing...")
                    time.sleep(0.1)  # Brief pause
                    continue
            
            continue
        
        # Detect objects
        detections = tracker.detect_objects(frame)
        
        # Update tracks
        tracks = tracker.update_tracks(detections, frame)
        
        # Draw results
        frame = tracker.draw_detections(frame, tracks)
        frame = tracker.draw_info(frame)
        
        # Update FPS
        tracker.update_fps()
        
        # Display
        if tracker.gui_available:
            cv2.imshow("Object Tracking", frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.info("Quit command received")
                break
            elif key == ord('r'):
                logger.info("Reset tracking")
                tracker.selected_track_id = None
                tracker.roi = None
                tracker.roi_center = None
                tracker.tracker = DeepSort(max_age=DEEPSORT_MAX_AGE, n_init=DEEPSORT_N_INIT)
        else:
            # No GUI - just log progress and check for quit signal
            if frame_count % 30 == 0:  # Log every 30 frames (~1 second at 30fps)
                logger.info(f"Processing frame {frame_count} - Tracking {len(tracks)} objects")
            
            # Check for quit (can't use cv2.waitKey without GUI)
            try:
                # Non-blocking check for keyboard input (limited in headless mode)
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'q':
                        logger.info("Quit command received")
                        break
                    elif key == b'r':
                        logger.info("Reset tracking")
                        tracker.selected_track_id = None
                        tracker.roi = None
                        tracker.roi_center = None
                        tracker.tracker = DeepSort(max_age=DEEPSORT_MAX_AGE, n_init=DEEPSORT_N_INIT)
            except ImportError:
                # msvcrt not available on non-Windows
                pass
    
    # Cleanup
    logger.info(f"Processed {frame_count} frames")
    cap.release()
    cv2.destroyAllWindows()
    logger.info("Tracking session ended")


if __name__ == "__main__":
    main()
