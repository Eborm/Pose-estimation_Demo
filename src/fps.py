import time
import cv2

class fps_counter:
    def __init__(self, offset = 0):
        self.start_time = time.time()
        self.last_time = 1.0
        self.fps_dict = {"time_stamp": "fps"}
        self.offset = offset
        self.fps_display = 0

    def calculate_fps(self):
        to_remove = []
        fps = 1.0 / (self.start_time - self.last_time)
        self.fps_dict[time.time()] = fps
        self.fps_display = 0
        for fps_time in list(self.fps_dict.keys()):
            if fps_time != "time_stamp":
                if fps_time < time.time() - 1:
                    to_remove.append(fps_time)
                else:
                    self.fps_display += self.fps_dict[fps_time]

        for fps_time_remove in to_remove:
            self.fps_dict.pop(fps_time_remove)

        if len(self.fps_dict) > 1:
            self.fps_display /= len(self.fps_dict) - 1

        self.last_time = self.start_time
        self.start_time = time.time()
    def draw_fps(self, frame, extra_text = ""):
        cv2.putText(frame, f'{extra_text} FPS: {int(self.fps_display)}', (10, 30 + self.offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
