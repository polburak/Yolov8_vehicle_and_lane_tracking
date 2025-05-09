import cv2
import json
import numpy as np

video_path = "input/video1.mp4"
lane_json_path = "lanes/lanes.json"

# Load lanes
with open(lane_json_path, "r") as f:
    lanes = json.load(f)

# Read first frame
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
cap.release()

if not ret:
    print("Failed to read video.")
    exit()

# Draw polygons
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

for i, lane in enumerate(lanes):
    pts = np.array(lane["points"], np.int32)
    cv2.polylines(frame, [pts], isClosed=True, color=colors[i % len(colors)], thickness=2)

    # Write label
    center = np.mean(pts, axis=0).astype(int)
    cv2.putText(frame, f"Lane {lane['lane_id']}", tuple(center),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, colors[i % len(colors)], 2)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        for lane in lanes:
            polygon = np.array(lane["points"], dtype=np.int32)
            if cv2.pointPolygonTest(polygon, point, False) >= 0:
                print(f"Point ({x}, {y}) is inside Lane {lane['lane_id']}.")
                return
        print(f"Point ({x}, {y}) is not inside any lane!")

cv2.namedWindow("Lane Verification")
cv2.setMouseCallback("Lane Verification", mouse_callback)

while True:
    cv2.imshow("Lane Verification", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
