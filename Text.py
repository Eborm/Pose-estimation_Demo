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
        for i in range(0, len(self.seperated_text)):
            if i%37 == 0:
                if i != 0:
                    self.seperated_text.insert(i, "\n")
        

    def draw(self, frame):
        y_offset = 0
        for line in self.animated_text.split("\n"):
            line = list(line)
            if len(line)> 1 and line[0] == " ":
                line.pop(0)
            line = "".join(line)

            cv2.putText(frame, line, (self.x, self.y + y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.text_color, 2)
            y_offset += 30

    def animation(self):
        if self.start_time is None:
            self.start_time = time.time()
        delta = time.time() - self.start_time
        chars_to_show = int(delta / self.seconds_per_word)
        chars_to_show = min(chars_to_show, len(self.seperated_text))
        self.animated_text = "".join(self.seperated_text[:chars_to_show])
