import cv2
import os
from modules.detector import detect
from modules.tracker import Tracker
from modules.logger import Logger
from modules.lane_loader import LaneLoader

video_path = "input/video1.mp4"
video_name = os.path.basename(video_path)
video_base = os.path.splitext(video_name)[0]
output_video_path = f"output/{video_base}_result.mp4"
log_path = f"output/{video_base}_log.txt"

cap = cv2.VideoCapture(video_path)
width, height = int(cap.get(3)), int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

os.makedirs("output", exist_ok=True)
out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

tracker = Tracker()
logger = Logger(log_path)
lane_loader = LaneLoader("lanes/lanes.json")

line_y = height // 2 + 150
frame_no = 0
crossed_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_no += 1
    detections = detect(frame)
    tracked_objects, history = tracker.update(detections, frame_no)

    for obj_id, (x1, y1, x2, y2) in tracked_objects.items():
        logger.mark_detected(obj_id)
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        lane_label = "Lane: -"

        if obj_id in history and len(history[obj_id]) >= 2:
            prev_cy = history[obj_id][-2][1]

            if obj_id not in crossed_ids:
                timestamp = frame_no / fps
                crossed_lane = lane_loader.find_lane(cx, cy)

                if prev_cy < line_y and cy >= line_y:
                    logger.mark_incoming(obj_id, crossed_lane, timestamp)
                    logger.count_lane(obj_id, crossed_lane)
                    crossed_ids.add(obj_id)

                elif prev_cy > line_y and cy <= line_y:
                    logger.mark_outgoing(obj_id, crossed_lane, timestamp)
                    logger.count_lane(obj_id, crossed_lane)
                    crossed_ids.add(obj_id)
                else:
                    lane_no = lane_loader.find_lane(cx, cy)
                    lane_label = f"Lane: {lane_no}" if lane_no else "Lane: ?"
            else:
                lane_label = "Lane: -"
        else:
            lane_no = lane_loader.find_lane(cx, cy)
            lane_label = f"Lane: {lane_no}" if lane_no else "Lane: ?"

        # Draw visuals
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {obj_id}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, lane_label, (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    # Draw counters
    counters = logger.get_summary()
    cv2.putText(frame, f"Incoming: {counters['incoming']} vehicles", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, f"Outgoing: {counters['outgoing']} vehicles", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Draw per-lane counters
    offset = 120
    for lane_id in sorted(counters["lanes"].keys()):
        count = counters["lanes"][lane_id]

        # Color for different sides
        if lane_id in [1, 2, 3]:
            color = (0, 0, 0)
        elif lane_id in [4, 5, 6]:
            color = (0, 0, 255)

        cv2.putText(frame, f"Lane {lane_id}: {count} vehicles", (10, offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        offset += 25

    # Horizontal line
    cv2.line(frame, (0, line_y), (width, line_y), (0, 0, 255), 2)

    out.write(frame)
    cv2.imshow(video_name, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

logger.write_log()
cap.release()
out.release()
cv2.destroyAllWindows()
