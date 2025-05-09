import cv2
import json
import os
import numpy as np

video_path = "input/video1.mp4"
lane_save_path = "lanes/lanes.json"
os.makedirs("lanes", exist_ok=True)

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
if not ret:
    print("Failed to read video!")
    exit()

draw_frame = frame.copy()
lanes = []
temp_points = []
current_lane = 1

def mouse_callback(event, x, y, flags, param):
    global temp_points, draw_frame, current_lane

    if event == cv2.EVENT_LBUTTONDOWN:
        temp_points.append((x, y))
        cv2.circle(draw_frame, (x, y), 4, (0, 255, 0), -1)

    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(temp_points) >= 3:
            lanes.append({
                "lane_id": current_lane,
                "points": temp_points
            })
            print(f"[OK] Lane {current_lane} saved.")
            current_lane += 1
            temp_points = []
            draw_frame = frame.copy()
            for lane in lanes:
                pts = lane["points"]
                cv2.polylines(draw_frame, [np.array(pts, np.int32)], isClosed=True, color=(255, 0, 0), thickness=2)
        else:
            print("You must draw a polygon with at least 3 points!")

cv2.namedWindow("Lane Drawing")
cv2.setMouseCallback("Lane Drawing", mouse_callback)

while True:
    display = draw_frame.copy()

    # Draw temporary lines
    if len(temp_points) >= 2:
        for i in range(1, len(temp_points)):
            cv2.line(display, temp_points[i - 1], temp_points[i], (0, 255, 0), 1)

    cv2.putText(display, f"Click points for Lane {current_lane}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(display, "Right click to finish polygon", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    cv2.imshow("Lane Drawing", display)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if current_lane > 6:
        print("6 lanes drawn, process complete.")
        break

cap.release()
cv2.destroyAllWindows()

# Save to JSON
with open(lane_save_path, "w") as f:
    json.dump(lanes, f, indent=2)

print(f"Lanes successfully saved to '{lane_save_path}'")
