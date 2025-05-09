import math

class Tracker:
    def __init__(self):
        self.next_id = 0
        self.tracks = {}
        self.history = {}

    def update(self, detections, frame_no):
        new_tracks = {}

        for x1, y1, x2, y2 in detections:
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            matched_id = None
            for obj_id, (px1, py1, px2, py2) in self.tracks.items():
                pcx = (px1 + px2) // 2
                pcy = (py1 + py2) // 2
                distance = math.hypot(cx - pcx, cy - pcy)
                if distance < 50:
                    matched_id = obj_id
                    break

            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1

            new_tracks[matched_id] = (x1, y1, x2, y2)
            self.history.setdefault(matched_id, []).append((cx, cy, frame_no))

        self.tracks = new_tracks
        return self.tracks, self.history
