"""
Multi-Object Tracking System using YOLOv8 and DeepSORT
Displays live tracking results in video feed with object IDs
"""

import cv2
import time
import logging
from ultralytics import YOLO
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
        logger.info(f"Loading YOLO model: {model_name}")
        self.model = YOLO(model_name)
        self.class_names = self.model.names
        self.confidence = confidence
        
        logger.info("Initializing DeepSORT tracker")
        self.tracker = DeepSort(max_age=DEEPSORT_MAX_AGE, n_init=DEEPSORT_N_INIT)
        
        # Tracking state
        self.selected_track_id = None
        self.roi = None
        self.roi_center = None
        self.fps = 0
        self.fps_time = time.time()
        
        logger.info("ObjectTracker initialized successfully")
    
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
                    conf = track.det_conf if hasattr(track, 'det_conf') else 0.0
                    text += f" | {conf:.2f}"
                
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
            cv2.imshow("Object Tracking", tracker.draw_info(frame))
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):
                tracker.roi = tracker.select_roi(frame)
                rx, ry, rw, rh = tracker.roi
                tracker.roi_center = (rx + rw/2, ry + rh/2)
            elif key == ord('q'):
                logger.info("Quit command received")
                break
            
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
    
    # Cleanup
    logger.info(f"Processed {frame_count} frames")
    cap.release()
    cv2.destroyAllWindows()
    logger.info("Tracking session ended")


if __name__ == "__main__":
    main()
