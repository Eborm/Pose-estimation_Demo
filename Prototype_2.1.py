import cv2
import mediapipe as mp
import os
import time
import threading
from Classes import Button

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)



button_x, button_y, button_w, button_h = 100, 100, 150, 50


POSE_COLOR = (0, 255, 0)
HAND_COLOR = (255, 0, 0)
FACE_COLOR = (0, 0, 255)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic, \
     mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        button_1 = Button(frame, "Test knop",100, 100, 150, 50, (0, 255, 0), (0, 200, 0), lambda: os.system("start chrome.exe"))
        button_2 = Button(frame, "Elon Musk banaan", 1000 ,100, 225, 50, (0, 255, 0), (0, 200, 0), lambda: os.system("start chrome.exe https://www.youtube.com/watch?v=-VfYjPzj1Xw"))
        #cv2.rectangle(frame, (1100, 0), (1800, 1080), (0, 0, 0), -1)
        h, w, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = holistic.process(rgb_frame)
        hand_results = hands.process(rgb_frame)

        button_1.draw()
        button_2.draw()

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

        button_1.check_hover(hand_results, h, w)
        button_2.check_hover(hand_results, h, w)
                    

        cv2.imshow('Pose & Handtracking met Knop Interactie', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
