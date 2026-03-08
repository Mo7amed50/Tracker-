import cv2
import time
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLO pretrained model
model = YOLO("yolov8n.pt")

# Get YOLO class names
class_names = model.names

# Initialize DeepSORT
tracker = DeepSort(max_age=30)

cap = cv2.VideoCapture(0)

selected_track_id = None
roi = None
roi_center = None

fps_time = time.time()

while True:

    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for speed
    frame = cv2.resize(frame, (960, 540))
    if roi is None:

        cv2.putText(frame,
                    "Press 's' to select object",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,255),
                    2)

        cv2.imshow("Object Tracking", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            roi = cv2.selectROI("Object Tracking", frame, False)
            rx, ry, rw, rh = roi
            roi_center = (rx + rw/2, ry + rh/2)

        if key == ord("q"):
            break

        continue

    results = model(frame)[0]

    detections = []

    for box in results.boxes:

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = float(box.conf[0])
        cls = int(box.cls[0])

        detections.append(([x1, y1, x2-x1, y2-y1], conf, cls))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = track.to_ltrb()

        cx = (l+r)/2
        cy = (t+b)/2

        # Identify the selected object
        if selected_track_id is None and roi_center is not None:
            if abs(cx - roi_center[0]) < rw and abs(cy - roi_center[1]) < rh:
                selected_track_id = track_id

        # Draw only selected object
        if track_id == selected_track_id:

            x1, y1, x2, y2 = int(l), int(t), int(r), int(b)

            # Get object class name
            cls_id = track.det_class
            label = class_names[cls_id] if cls_id is not None else "Object"

            # Draw bounding box
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)

            # Label background
            cv2.rectangle(frame,(x1,y1-30),(x1+220,y1),(0,255,0),-1)

            # Display name + ID
            cv2.putText(frame,
                        f"{label} | ID:{track_id}",
                        (x1+5,y1-8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,0,0),
                        2)

    new_time = time.time()
    fps = 1/(new_time - fps_time)
    fps_time = new_time

    cv2.putText(frame,
                f"FPS: {int(fps)}",
                (20,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,0),
                2)

    cv2.imshow("Object Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()