import cv2
import mediapipe as mp
import os
import time

class ColorBGR:
    def __init__(self, b, g, r):
        self.b = b
        self.g = g
        self.r = r

    def to_tuple(self):
        return (self.b, self.g, self.r)
    
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)

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
        cv2.rectangle(frame, self.pos.to_tuple(), (self.pos.x + self.size.x, self.pos.y + self.size.y), self.color.to_tuple(), -1)
        cv2.putText(frame, self.text, (self.pos.x + 10, self.pos.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.text_color.to_tuple(), 2)

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

start_time = time.time()
fps_count = 0
fps_count_temp = 0

def draw_fps():
    global start_time
    global fps_count
    global fps_count_temp

    if time.time() - start_time < 1:
        fps_count_temp += 1
    elif time.time() - start_time > 1:
        start_time = time.time()
        fps_count = fps_count_temp
        fps_count_temp = 0

    cv2.putText(frame, f'FPS: {fps_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def draw(frame, texts, buttons):
    #ui design
    cv2.rectangle(frame, (1480, 0), (1920, 1080), (52, 27, 237), -1)
    #img
    cv2.rectangle(frame, (1500, 20), (1900, 420), (255, 255, 255), -1)
    #txt
    cv2.rectangle(frame, (1500, 440), (1900, 1060), (255, 255, 255), -1)   

    for text in texts:
        text.animation()
        text.draw(frame)

    for button in buttons:
        button.draw(frame)

    draw_fps()

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

POSE_COLOR = ColorBGR(0, 255, 0)
HAND_COLOR = ColorBGR(255, 0, 0)
FACE_COLOR = ColorBGR(0, 0, 255)

BUTTON_TEXT_COLOR = ColorBGR(255, 255, 255)
TEXT_COLOR = ColorBGR(0, 0, 0)
BUTTON_COLOR = ColorBGR(0, 0, 0)
BUTTON_HOVER_COLOR = ColorBGR(0, 0, 255)
BUTTON_1_POS = Vector2(100, 100)
BUTTON_2_POS = Vector2(1000, 100)
BUTTON_SIZE = Vector2(225, 50)
TEXT_1_POS = Vector2(1500, 460)

buttons = []
texts = []

button_1 = Button(
    "Test knop",
    BUTTON_TEXT_COLOR,
    BUTTON_1_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: os.system("start chrome.exe")
)

button_2 = Button(
    "Website",
    BUTTON_TEXT_COLOR,
    BUTTON_2_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: os.system("start chrome.exe")
)

text_1 = Text(
    "Dit is een tekst. Dit is een tekst. Dit is een tekst",
    TEXT_COLOR,
    TEXT_1_POS
)

buttons.append(button_1)
buttons.append(button_2)
texts.append(text_1)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic, \
     mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = holistic.process(rgb_frame)
        hand_results = hands.process(rgb_frame)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=POSE_COLOR.to_tuple(), thickness=2, circle_radius=3),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

        if result.left_hand_landmarks:
            mp_drawing.draw_landmarks(frame, result.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=HAND_COLOR.to_tuple(), thickness=2, circle_radius=3),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

        if result.right_hand_landmarks:
            mp_drawing.draw_landmarks(frame, result.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=HAND_COLOR.to_tuple(), thickness=2, circle_radius=3),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

        if result.face_landmarks:
            mp_drawing.draw_landmarks(frame, result.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                      mp_drawing.DrawingSpec(color=FACE_COLOR.to_tuple(), thickness=1, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1))

        draw(frame, texts, buttons)

        button_1.button_handler(hand_results, h, w)
        button_2.button_handler(hand_results, h, w)

        cv2.imshow('Pose Estimator', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()