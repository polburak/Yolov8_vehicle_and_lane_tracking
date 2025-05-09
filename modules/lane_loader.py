import json
import os
import cv2
import numpy as np

class LaneLoader:
    def __init__(self, file_path="lanes/lanes.json"):
        self.lanes = []
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Lane file not found: {file_path}")
        with open(file_path, "r") as f:
            self.lanes = json.load(f)

    def find_lane(self, cx, cy):
        point = (cx, cy)
        for lane in self.lanes:
            polygon = np.array(lane["points"], dtype=np.int32)
            if cv2.pointPolygonTest(polygon, point, False) >= 0:
                return lane["lane_id"]
        return None
