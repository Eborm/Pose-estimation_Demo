import cv2
import mediapipe as mp
import os
import time
from button import Button
from text import Text
from color import ColorBGR
from vector2 import Vector2
from cv2_interface import draw_rectangle, draw_text
from image import image



start_time = time.time()
active_level = 0
last_time = 1.0
fps_dict = {"time_stamp": "fps"}

def draw_fps(frame):
    to_remove = []
    global fps_old
    global start_time
    global last_time
    fps = 1.0 / (start_time - last_time)
    fps_dict[time.time()] = fps
    fps_display = 0
    for fps_time in fps_dict:
        if fps_time != "time_stamp":
            if fps_time < time.time() - 1:
                to_remove.append(fps_time)
            else:
                fps_display += fps_dict[fps_time]
    for fps_time_remove in to_remove:
        fps_dict.pop(fps_time_remove)
    fps_display /= len(fps_dict) - 1
    last_time = start_time
    start_time = time.time()
    cv2.putText(frame, f'FPS: {int(fps_display)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def change_active_level(level):
    global active_level
    texts[active_level].start_time = None
    active_level = level

def draw(frame, texts, buttons):
    # Right panel
    cv2.rectangle(frame, (1480, 0), (1920, 1080), (52, 27, 237), -1)
    # Image panel (top right)
    cv2.rectangle(frame, (1500, 20), (1900, 420), (255, 255, 255), -1)
    # Explanation panel (bottom right)
    cv2.rectangle(frame, (1500, 440), (1900, 1060), (255, 255, 255), -1)   

    texts[active_level].animation()
    texts[active_level].draw(frame)
    
    for button in buttons:
        button.draw(frame)

    images[active_level].draw(frame)

    draw_fps(frame)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
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
BUTTON_3_POS = Vector2(100, 500)
BUTTON_4_POS = Vector2(1000, 500)
BUTTON_SIZE = Vector2(200, 50)
TEXT_1_POS = Vector2(1500, 460)


buttons = []
texts = []
images = []

button_1 = Button(
    "pose-estimation",
    BUTTON_TEXT_COLOR,
    BUTTON_1_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: change_active_level(1)
)

button_2 = Button(
    "sport",
    BUTTON_TEXT_COLOR,
    BUTTON_2_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: change_active_level(2)
)

button_3 = Button(
    "gaming",
    BUTTON_TEXT_COLOR,
    BUTTON_3_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: change_active_level(3)
)

button_4 = Button(
    "medicijn",
    BUTTON_TEXT_COLOR,
    BUTTON_4_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: change_active_level(4)
)

text_1 = Text(
    "Welkom bij de Pose Estimation Demonstrator. Voor informatie over de vakgebieden. " \
    "Beweeg je hand naar een van de 4 vakjes en houd vast totdat het vakje volledig rood is.",
    TEXT_COLOR,
    TEXT_1_POS
)

text_2 = Text(
    "Pose estimation is een techniek waarmee automatisch de houding van een persoon wordt herkend aan de hand van camerabeelden." \
    " Hierbij worden belangrijke punten op het lichaam, zoals de schouders, knieën en heupen, opgespoord." \
    " Op basis van deze punten kan de beweging of houding van een persoon in kaart worden gebracht.",
    TEXT_COLOR,
    TEXT_1_POS
)

text_3 = Text(
    "Pose estimation speelt een steeds grotere rol binnen de sportwereld." \
    " Door middel van camerabeelden en slimme software kunnen lichaamsbewegingen automatisch herkend en geanalyseerd worden." \
    " Dit maakt het mogelijk om de houding en techniek van een sporter nauwkeurig te volgen, zonder dat hiervoor speciale sensoren nodig zijn.",
    TEXT_COLOR,
    TEXT_1_POS
)

text_4 = Text(
    "Pose estimation wordt ook in de gamewereld steeds vaker toegepast." \
    " Met deze technologie kunnen games bestuurd worden door lichaamsbewegingen in plaats van met een controller of toetsenbord." \
    " De camera herkent automatisch de houding en beweging van de speler en vertaalt dit naar acties in het spel." \
    " Games die deze technologie zijn bijvoorbeeld 'Just Dance' en 'Kinect Sport'",
    TEXT_COLOR,
    TEXT_1_POS
)

text_5 = Text(
    "In de medische wereld biedt pose estimation waardevolle mogelijkheden voor het analyseren van beweging en lichaamshouding." \
    " Deze technologie kan worden ingezet bij diagnose, revalidatie en het monitoren van de voortgang van patiënten," \
    " zonder dat er dure of invasieve apparatuur nodig is." \
    " Een specifiek voorbeeld is het gebruik van pose estimation bij juveniele dermatomyositis (JDM)," \
    " een zeldzame auto-immuunziekte bij kinderen die spierzwakte veroorzaakt." \
    " Bij JDM is het belangrijk om de spierfunctie goed te volgen, met name bij bewegingen zoals opstaan," \
    " hurken of het optillen van de armen.",
    TEXT_COLOR,
    TEXT_1_POS
)

image_0 = image("../assets/zuyd_logo.png", Vector2(1500,20), Vector2(400, 400))
image_1 = image("../assets/pose-estimation.png", Vector2(1500,20), Vector2(400, 400))
image_2 = image("../assets/sport-application.png", Vector2(1500,20), Vector2(400, 400))
image_3 = image("../assets/game-application.png" , Vector2(1500,20), Vector2(400, 400))
image_4 = image("../assets/health-application.png", Vector2(1500,20), Vector2(400, 400))

buttons.append(button_1)
buttons.append(button_2)
buttons.append(button_3)
buttons.append(button_4)
texts.append(text_1)
texts.append(text_2)
texts.append(text_3)
texts.append(text_4)
texts.append(text_5)
images.append(image_0)
images.append(image_1)
images.append(image_2)
images.append(image_3)
images.append(image_4)

pose_spec = mp_drawing.DrawingSpec(color=POSE_COLOR.to_tuple(), thickness=2, circle_radius=3)
hand_spec = mp_drawing.DrawingSpec(color=HAND_COLOR.to_tuple(), thickness=2, circle_radius=3)
face_spec = mp_drawing.DrawingSpec(color=FACE_COLOR.to_tuple(), thickness=2, circle_radius=3)
white_spec = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)

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
            mp_drawing.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                pose_spec,
                white_spec
            )

        if result.left_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                result.left_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                hand_spec,
                white_spec
            )

        if result.right_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                result.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                hand_spec,
                white_spec
            )


        draw(frame, texts, buttons)

        button_1.button_handler(hand_results, h, w)
        button_2.button_handler(hand_results, h, w)
        button_3.button_handler(hand_results, h, w)
        button_4.button_handler(hand_results, h, w)

        cv2.imshow('Pose Estimator', frame)
        frame_counter += 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
