import time
import cv2
from color import ColorBGR
from vector2 import Vector2
from cv2_interface import draw_text
import textwrap

class Text:
    def __init__(self, text, text_color, pos, animation_duration=3):
        self.text_color = text_color # ColorBGR
        self.pos = pos # Vector2
        self.animation_duration = animation_duration # Int
        self.seperated_text = list(text) # String
        self.seconds_per_word = self.animation_duration / len(self.seperated_text)
        self.start_time = None
        self.animated_text = ""

        self.seperated_text = list("\n".join(textwrap.wrap(text, 32)))

    def draw(self, frame):
        for i, line in enumerate(self.animated_text.split("\n")):
            draw_text(frame, line.strip(), Vector2(self.pos.x, self.pos.y + i * 30), self.text_color, 2)


    def animation(self):
        if self.start_time is None:
            self.start_time = time.time()
        dt = time.time() - self.start_time
        chars_to_show = int(dt / self.seconds_per_word)
        chars_to_show = min(chars_to_show, len(self.seperated_text))
        self.animated_text = "".join(self.seperated_text[:chars_to_show])