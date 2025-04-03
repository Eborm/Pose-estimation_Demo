import cv2
import time

class Button:
    def __init__(self, text, text_color, x, y, width, height, color, hover_color, action=None, cooldown_time=2, cooldown_hover=3):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.standard_color = color
        self.hover_color = hover_color
        self.action = action
        self.cooldown_time = cooldown_time
        self.cooldown_enabled = False
        self.cooldown_start_time = None
        self.cooldown_hover = cooldown_hover
        self.cooldown_hover_enabled = False
        self.cooldown_hover_start_time = None
        self.text_color = text_color

        # berekenen van verschil tussen standaard kleur en hover kleur en increment van de kleuren per 0.1 seconde
        b_standard, g_standard, r_standard = self.standard_color
        b_target, g_target, r_target = self.hover_color
        self.b_diff = b_target - b_standard
        self.g_diff = g_target - g_standard
        self.r_diff = r_target - r_standard
        self.b_inc = self.b_diff / cooldown_hover if self.b_diff != 0 else 0
        self.g_inc = self.g_diff / cooldown_hover if self.g_diff != 0 else 0
        self.r_inc = self.r_diff / cooldown_hover if self.r_diff != 0 else 0


    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), self.color, -1)
        cv2.putText(frame, self.text, (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.text_color, 2)

    def check_hover(self, hand_results, h, w):
        self.color = self.standard_color

        if self.cooldown_enabled:
            if time.time() - self.cooldown_start_time > self.cooldown_time:
                self.cooldown_enabled = False
        elif hand_results.multi_hand_landmarks and not self.cooldown_enabled:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if self.x < cx < self.x + self.width and self.y < cy < self.y + self.height:
                        if self.action and self.cooldown_hover_enabled:
                            self.cooldown_start_time = time.time()
                            self.cooldown_enabled = True
                            self.cooldown_hover_enabled = False
                            self.color = self.standard_color
                            self.action()
                        elif not self.cooldown_hover_enabled:
                            self.animate_color()
                            if self.cooldown_hover_start_time is None:
                                self.cooldown_hover_start_time = time.time()
                            elif time.time() - self.cooldown_hover_start_time > self.cooldown_hover:
                                self.cooldown_hover_enabled = True
                                self.cooldown_hover_start_time = None

        if self.color == self.standard_color:
            self.cooldown_hover_start_time = None

    def animate_color(self):
        if self.cooldown_hover_start_time is not None:
            elapsed_time = time.time() - self.cooldown_hover_start_time
            if elapsed_time == 0:
                elapsed_time = 0.1
            new_b = max(0, min(255, int(self.standard_color[0] + self.b_inc * elapsed_time)))
            new_g = max(0, min(255, int(self.standard_color[1] + self.g_inc * elapsed_time)))
            new_r = max(0, min(255, int(self.standard_color[2] + self.r_inc * elapsed_time)))
            self.color = (new_b, new_g, new_r)
