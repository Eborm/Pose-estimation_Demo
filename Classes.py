import cv2
import os
import time

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None, cooldown_time=2, cooldown_hover=3):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.standard_color = color
        self.hover_color = hover_color
        self.action = action
        self.cooldown_time=cooldown_time
        self.cooldown_eneabled = False
        self.cooldown_start_time = None
        self.cooldown_hover = cooldown_hover
        self.cooldown_hover_enabled = False
        self.cooldown_hover_start_time = None

    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), self.color, -1)
        cv2.putText(frame, self.text, (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    def check_hover(self, hand_results, h, w):
        if self.cooldown_eneabled:
            if time.time() - self.cooldown_start_time > self.cooldown_time:
                    self.cooldown_eneabled = False
        elif hand_results.multi_hand_landmarks and self.cooldown_eneabled == False:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if self.x < cx < self.x + self.width and self.y < cy < self.y + self.height:
                        print("Knop ingedrukt! Venster openen...")
                        if self.action != None and self.cooldown_hover_enabled == True:
                            self.cooldown_start_time = time.time()
                            self.cooldown_eneabled = True
                            self.cooldown_hover_enabled = False
                            self.color = self.standard_color
                            self.action()
                        elif not self.cooldown_hover_enabled:
                            self.color = (0, 0, 255)
                            if self.cooldown_hover_start_time == None:
                                self.cooldown_hover_start_time = time.time()
                            elif time.time() - self.cooldown_hover_start_time > self.cooldown_hover:
                                self.cooldown_hover_enabled = True
                                self.cooldown_hover_start_time = None


class Text:
    def __init__(self, frame, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.frame = frame

    def draw(self):
        cv2.putText(self.frame, self.text, (self.x, self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (self.color), 2)