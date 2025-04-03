import cv2
import mediapipe as mp
import os
import time
import threading
from Button_v2 import Button
from Text import Text

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cv2.namedWindow("Pose & Handtracking met Knop Interactie", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Pose & Handtracking met Knop Interactie", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

POSE_COLOR = (0, 255, 0)
HAND_COLOR = (255, 0, 0)
FACE_COLOR = (0, 0, 255)
button_1 = Button("Test knop", (255, 255, 255), 100, 100, 150, 50, (0, 0, 0), (0, 0, 255), lambda: os.system("start chrome.exe"))
button_2 = Button("Website", (255, 255, 255), 1000 ,100, 225, 50, (0, 0, 0), (0, 0, 255), lambda: os.system("start chrome.exe https://chat.daan.engineer/"))
text_1  = Text("Dit is een test tekst. Dit is een test tekst. Dit is een test tekst", (0, 0, 0), 1500, 460)

def teken():
    #ui design
    cv2.rectangle(frame, (1480, 0), (1920, 1080), (52, 27, 237), -1)
    #img
    cv2.rectangle(frame, (1500, 20), (1900, 420), (255, 255, 255), -1)
    #txt
    cv2.rectangle(frame, (1500, 440), (1900, 1060), (255, 255, 255), -1)   
    text_1.animation()
    #button_2.draw(frame)
    text_1.draw(frame)


start_time = time.time()
fps_count = 0
fps_count_temp = 0

def fps():
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

        button_1.draw(frame)
        fps()

        tekenthread = threading.Thread(target = teken)
        tekenthread.start()

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=POSE_COLOR, thickness=2, circle_radius=3),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

        if result.left_hand_landmarks:
            mp_drawing.draw_landmarks(frame, result.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=HAND_COLOR, thickness=2, circle_radius=3),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

        if result.right_hand_landmarks:
            mp_drawing.draw_landmarks(frame, result.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=HAND_COLOR, thickness=2, circle_radius=3),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

        if result.face_landmarks:
            mp_drawing.draw_landmarks(frame, result.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                      mp_drawing.DrawingSpec(color=FACE_COLOR, thickness=1, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1))

        button_1.button_handler(hand_results, h, w)
        #button_2.button_handler(hand_results, h, w)

        cv2.imshow('Pose & Handtracking met Knop Interactie', frame)

        tekenthread.join()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
