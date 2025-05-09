import os
from collections import defaultdict

class Logger:
    def __init__(self, file_path):
        self.detected_ids = set()
        self.incoming_counter = 0
        self.outgoing_counter = 0
        self.lane_counters = defaultdict(int)
        self.passage_times = []  # (id, direction, lane, time)
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def mark_detected(self, obj_id):
        self.detected_ids.add(obj_id)

    def mark_incoming(self, obj_id, lane_id=None, time=None):
        if obj_id in self.detected_ids:
            self.incoming_counter += 1
            if time is not None:
                self.passage_times.append((obj_id, "Incoming", lane_id, time))

    def mark_outgoing(self, obj_id, lane_id=None, time=None):
        if obj_id in self.detected_ids:
            self.outgoing_counter += 1
            if time is not None:
                self.passage_times.append((obj_id, "Outgoing", lane_id, time))

    def count_lane(self, obj_id, lane_id):
        if obj_id in self.detected_ids and lane_id is not None:
            self.lane_counters[lane_id] += 1

    def get_summary(self):
        return {
            "total": len(self.detected_ids),
            "incoming": self.incoming_counter,
            "outgoing": self.outgoing_counter,
            "lanes": dict(self.lane_counters)
        }

    def write_log(self):
        with open(self.file_path, 'w') as f:
            f.write(f"=>Total Incoming Vehicles: {self.incoming_counter}\n\n")
            f.write(f"=>Total Outgoing Vehicles: {self.outgoing_counter}\n\n")
            f.write("=>Lane-Based Transitions:\n\n")
            for lane_id in sorted(self.lane_counters.keys()):
                f.write(f"  Lane {lane_id}: {self.lane_counters[lane_id]} vehicles\n")

            f.write("\n=>Vehicle Passage Times:\n\n")
            for obj_id, direction, lane_id, time in self.passage_times:
                f.write(f"ID: {obj_id} | Direction: {direction} | Lane: {lane_id} | Time: {time:.2f} seconds\n")
