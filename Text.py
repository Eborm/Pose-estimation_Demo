import cv2
import time

class Text():
    def __init__(self, text, text_color, x, y, animation_duration=3):
        self.text_color = text_color
        self.x = x
        self.y = y
        self.animation_duration = animation_duration
        self.seperated_text = list(text)
        self.seconds_per_word = self.animation_duration / len(self.seperated_text)
        self.start_time = None
        self.animated_text = "" 

    def draw(self, frame):
        cv2.putText(frame, self.animated_text, (self.x, self.y), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, self.text_color, 2)

    def animation(self):
        if self.start_time is None:
            self.start_time = time.time()
        delta = time.time() - self.start_time
        chars_to_show = int(delta / self.seconds_per_word)
        chars_to_show = min(chars_to_show, len(self.seperated_text))
        self.animated_text = "".join(self.seperated_text[:chars_to_show])
