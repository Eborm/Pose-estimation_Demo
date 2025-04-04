import time
import cv2
from Color import ColorBGR
from Vector2 import Vector2

class Text:
    def __init__(self, text, text_color, pos, animation_duration=3):
        self.text_color = text_color # ColorBGR
        self.pos = pos # Vector2
        self.animation_duration = animation_duration # Int
        self.seperated_text = list(text) # String
        self.seconds_per_word = self.animation_duration / len(self.seperated_text)
        self.start_time = None
        self.animated_text = ""

        for i in range(0, len(self.seperated_text)):
            if i % 37 == 0 and i != 0:
                self.seperated_text.insert(i, "\n")

    def draw(self, frame):
        y_offset = 0
        for line in self.animated_text.split("\n"):
            line = list(line)
            if len(line) > 1 and line[0] == " ":
                line.pop(0)
            line = "".join(line)

            cv2.putText(frame, line, (self.pos.x, self.pos.y + y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.text_color.to_tuple(), 2)
            y_offset += 30

    def animation(self):
        if self.start_time is None:
            self.start_time = time.time()
        dt = time.time() - self.start_time
        chars_to_show = int(dt / self.seconds_per_word)
        chars_to_show = min(chars_to_show, len(self.seperated_text))
        self.animated_text = "".join(self.seperated_text[:chars_to_show])