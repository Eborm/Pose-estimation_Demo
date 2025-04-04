import cv2
import mediapipe as mp
import os
import time
from button import Button
from text import Text
from color import ColorBGR
from vector2 import Vector2
from cv2_interface import draw_rectangle, draw_text

start_time = time.time()

def draw_fps():
    global start_time
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - start_time)
    start_time = cv2.getTickCount()
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


def draw(frame, texts, buttons):
    # Right panel
    cv2.rectangle(frame, (1480, 0), (1920, 1080), (52, 27, 237), -1)
    # Image panel (top right)
    cv2.rectangle(frame, (1500, 20), (1900, 420), (255, 255, 255), -1)
    # Explanation panel (bottom right)
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
cv2.namedWindow("Pose Estimator", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Pose Estimator", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


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
    lambda: os.system("start chrome.exe https://chat.daan.engineer/")
)

text_1 = Text(
    "Dit is een tekst. Dit is een tekst. Dit is een tekst",
    TEXT_COLOR,
    TEXT_1_POS
)

buttons.append(button_1)
buttons.append(button_2)
texts.append(text_1)

frame_skip = 2
frame_counter = 0

with mp_holistic.Holistic(static_image_mode=False, model_complexity=0,min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic, \
     mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        frame = cv2.resize(frame, (1920, 1080))
        button_h_detect, button_w_detect = 1920, 1080
        frame_small = cv2.resize(frame, (w//2, h//2))
        if frame_counter % frame_skip == 0:
            rgb_frame = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)

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

        draw(frame, texts, buttons)

        button_1.button_handler(hand_results, h, w)
        button_2.button_handler(hand_results, h, w)

        cv2.imshow('Pose Estimator', frame)
        frame_counter += 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()