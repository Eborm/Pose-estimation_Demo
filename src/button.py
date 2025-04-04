import time
import cv2
from cv2_interface import draw_rectangle, draw_text
from color import ColorBGR
from vector2 import Vector2

class Button:
    def __init__(self, text, text_color, pos, size, color, hover_color, action=None):
        self.text = text # String
        self.text_color = text_color # ColorBGR
        self.pos = pos # Vector2
        self.size = size # Vector2
        self.color, self.standard_color = color, color # ColorBGR
        self.hover_color = hover_color # ColorBGR
        self.action = action # Lambda function

        self.cooldown_length = 2
        self.cooldown_enabled = False
        self.cooldown_start_time = None

        self.hover_cooldown_length = 3
        self.hover_enabled = False
        self.hover_start_time = None

        self.not_hovering = 6.0
        self.not_hovering_start_time = None

        b_stand, g_stand, r_stand = self.color.to_tuple()
        b_targ, g_targ, r_targ = self.hover_color.to_tuple()

        self.b_inc = (b_targ - b_stand) / self.hover_cooldown_length if (b_targ - b_stand) != 0 else 0
        self.g_inc = (g_targ - g_stand) / self.hover_cooldown_length if (g_targ - g_stand) != 0 else 0
        self.r_inc = (r_targ - r_stand) / self.hover_cooldown_length if (r_targ - r_stand) != 0 else 0

    def draw(self, frame):
        draw_rectangle(frame, self.pos, self.size, self.color, -1)
        draw_text(frame, self.text, Vector2(self.pos.x + 10, self.pos.y + 30), self.text_color, 2)

    def hover_time_handler(self):
        if self.hover_start_time == None:
            self.hover_start_time = time.time()
        elif time.time() - self.hover_start_time > self.hover_cooldown_length:
            self.hover_enabled = True
            self.hover_start_time = None

    def not_hovering_handler(self):
        if self.not_hovering_start_time == None:
            self.not_hovering_start_time = time.time()
        elif time.time() - self.not_hovering_start_time > self.not_hovering:
            self.not_hovering_start_time = None
            self.hover_start_time = None
            self.hover_enabled = False
            self.color = self.standard_color

    def button_cooldown_handler(self):
        self.cooldown_start_time = time.time()
        self.cooldown_enabled = True
        self.hover_enabled = False
        self.color = self.standard_color
        self.action()

    def animate_color(self):
        if self.hover_start_time == None:
            return
        
        elapsed_time = time.time() - self.hover_start_time

        if elapsed_time == 0:
            return
        
        new_b = max(0, min(255, int(self.standard_color.to_tuple()[0] + self.b_inc * elapsed_time)))
        new_g = max(0, min(255, int(self.standard_color.to_tuple()[1] + self.g_inc * elapsed_time)))
        new_r = max(0, min(255, int(self.standard_color.to_tuple()[2] + self.r_inc * elapsed_time)))

        self.color = ColorBGR(new_b, new_g, new_r)
    
    def button_handler(self, hand_results, h, w):
        if (self.cooldown_enabled) and \
           (time.time() - self.cooldown_start_time > self.cooldown_length):
            self.cooldown_enabled = False
        elif hand_results.multi_hand_landmarks and self.action != None:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if self.pos.x < cx < (self.pos.x + self.size.x) and self.pos.y < cy < (self.pos.y + self.size.y):
                        if self.hover_enabled:
                            self.button_cooldown_handler()
                        elif not self.hover_enabled:
                            self.animate_color()
                            self.hover_time_handler()
                    else:
                        self.not_hovering_handler()
