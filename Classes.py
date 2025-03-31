import cv2
import os
import time

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None, cooldowntime=2):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.cooldowntime=cooldowntime
        self.cooldowneneabled = False
        self.cooldownstarttime = None

    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), self.color, -1)
        cv2.putText(frame, self.text, (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    def check_hover(self, hand_results, h, w):
        if self.cooldowneneabled:
            print(time.time() - self.cooldownstarttime > self.cooldowntime)
            if time.time() - self.cooldownstarttime > self.cooldowntime:
                    self.cooldowneneabled = False
        if hand_results.multi_hand_landmarks and self.cooldowneneabled == False:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if self.x < cx < self.x + self.width and self.y < cy < self.y + self.height:
                        print("Knop ingedrukt! Venster openen...")
                        if self.action != None:
                            self.cooldownstarttime = time.time()
                            self.cooldowneneabled = True
                            self.action()
                        else:
                            print("geen actie aanwezig voor deze knop")
                        return


class Text:
    def __init__(self, frame, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.frame = frame

    def draw(self):
        cv2.putText(self.frame, self.text, (self.x, self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (self.color), 2)