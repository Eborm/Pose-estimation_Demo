import tensorflow as tf
tf.config.threading.set_intra_op_parallelism_threads(8)
tf.config.threading.set_inter_op_parallelism_threads(8)
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
import threading
import queue
from fps import fps_counter

active_level = 0

frame_queue = queue.Queue(maxsize=1)

hand_results = None
result = None
dark_mode = False

def change_active_level(level):
    global active_level
    global score
    global text_4
    if level == 3:
        score = score+10
    if level == 0:
        score = 0
    texts[active_level].start_time = None
    active_level = level

def dark_mode_handler():
    global dark_mode
    if dark_mode:
        dark_mode = False
    else:
        dark_mode = True

def draw(frame, texts, images, buttons):
    global dark_mode    
    if dark_mode:
      cv2.rectangle(frame, (0, 0), (1920, 1080), (0, 0, 0), -1)  
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
    fps_counter_fps.fps_display = score
    fps_counter_fps.draw_fps(frame)
    #fps_counter_mediapip.draw_fps(frame, " MEDIAPIPE")


def process_frame(frame_queue, holistic, hands, fps_counter):
    while True:
        global result
        global hand_results
        if not frame_queue.empty():
            frame = frame_queue.get()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = holistic.process(rgb_frame)
            hand_results = hands.process(rgb_frame)
            fps_counter.calculate_fps()
            
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
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
BUTTON_1_POS = Vector2(70, 100)
BUTTON_2_POS = Vector2(1210, 100)
BUTTON_3_POS = Vector2(70, 500)
BUTTON_4_POS = Vector2(1210, 500)
BUTTON_5_POS = Vector2(70, 900)
BUTTON_6_POS = Vector2(1210, 900)
BUTTON_SIZE = Vector2(200, 50)
TEXT_1_POS = Vector2(1500, 460)


buttons = []
texts = []
images = []

button_1 = Button(
    "Pose-Estimation",
    BUTTON_TEXT_COLOR,
    BUTTON_1_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: change_active_level(1)
)

button_2 = Button(
    "Sport",
    BUTTON_TEXT_COLOR,
    BUTTON_2_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: change_active_level(2)
)

button_3 = Button(
    "Gaming",
    BUTTON_TEXT_COLOR,
    BUTTON_3_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: change_active_level(3)
)

button_4 = Button(
    "Medisch",
    BUTTON_TEXT_COLOR,
    BUTTON_4_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR, 
    lambda: change_active_level(4)
)
button_5 = Button(
    "Terug",
    BUTTON_TEXT_COLOR,
    BUTTON_5_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    lambda: change_active_level(0)
)
button_6 = Button(
    "lampen uit",
    BUTTON_TEXT_COLOR,
    BUTTON_6_POS,
    BUTTON_SIZE,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    lambda: dark_mode_handler(),
    "lampen aan"
)


score :int =0
text_1 = Text(
    "Welkom bij de Pose Estimation Demonstrator. Voor informatie over de vakgebieden. " \
    "Beweeg de blauwe punten op je hand naar een van de 6 vakjes en houd vast totdat het vakje volledig rood is.",
    TEXT_COLOR,
    TEXT_1_POS
)
text_2 = Text(
    "Pose estimation is een techniek waarmee automatisch de houding van een persoon wordt herkend aan de hand van camerabeelden." \
    " Hierbij worden belangrijke punten op het lichaam, zoals de schouders, knieen en heupen, opgespoord." \
    " Op basis van deze punten kan de beweging of houding van een persoon in kaart worden gebracht.",
    TEXT_COLOR,
    TEXT_1_POS
)
text_3 = Text(
    "Pose estimation speelt een steeds grotere rol binnen de sportwereld." \
    " Door middel van camerabeelden en slimme software kunnen lichaamsbewegingen automatisch herkend en geanalyseerd worden." \
    f" Dit maakt het mogelijk om de houding en techniek van een sporter nauwkeurig te volgen, zonder dat hiervoor speciale sensoren nodig zijn.",
    TEXT_COLOR,
    TEXT_1_POS
)
text_4 = Text(
    "Pose estimation wordt ook in de gamewereld steeds vaker toegepast." \
    " Met deze technologie kunnen games bestuurd worden door lichaamsbewegingen in plaats van met een controller of toetsenbord." \
    " De camera herkent automatisch de houding en beweging van de speler en vertaalt dit naar acties in het spel." \
    f" Deze technologie wordt bevoorbeeld gebruikt in VR technologie om je handen te tracken. Score: {score}",
    TEXT_COLOR,
    TEXT_1_POS
)
text_5 = Text(
   "In de medische wereld biedt pose estimation waardevolle mogelijkheden voor het analyseren van beweging en lichaamshouding." \
    " Deze technologie kan worden ingezet bij diagnose, revalidatie en het monitoren van de voortgang van patienten," \
    " zonder dat er dure of invasieve apparatuur nodig is." \
    " Een specifiek voorbeeld is het gebruik van pose estimation bij juveniele dermatomyositis (JDM)," \
    " een zeldzame auto-immuunziekte bij kinderen die spierzwakte veroorzaakt." \
    " Bij JDM is het belangrijk om de spierfunctie goed te volgen, met name bij bewegingen zoals opstaan," \
    " hurken of het optillen van de armen.",
    TEXT_COLOR,
    TEXT_1_POS
)


image_0 = image("./assets/zuyd_logo.png", Vector2(1500,20), Vector2(400, 400))
image_1 = image("./assets/pose-estimation.png", Vector2(1500,20), Vector2(400, 400))
image_2 = image("./assets/sport-application.png", Vector2(1500,20), Vector2(400, 400))
image_3 = image("./assets/game-application.png" , Vector2(1500,20), Vector2(400, 400))
image_4 = image("./assets/health-application.png", Vector2(1500,20), Vector2(400, 400))

buttons.append(button_1)
buttons.append(button_2)
buttons.append(button_3)
buttons.append(button_4)
buttons.append(button_5)
buttons.append(button_6)
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

with mp_holistic.Holistic(static_image_mode=False, model_complexity=0,min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic, \
    mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    fps_counter_fps = fps_counter()
    fps_counter_mediapip = fps_counter(30)
    mediapipe_thread = threading.Thread(target=process_frame, args=(frame_queue, holistic, hands, fps_counter_mediapip))
    mediapipe_thread.start()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        frame = cv2.resize(frame, (1920, 1080))
        button_h_detect, button_w_detect = 1920, 1080
        frame_small = cv2.resize(frame, (w//2, h//2))
        if frame_queue.empty():
            frame_queue.put(frame_small)

        fps_counter_fps.calculate_fps()

        draw(frame, texts, images, buttons)
        if hand_results != None:
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

            button_1.button_handler(hand_results, h, w)
            button_2.button_handler(hand_results, h, w)
            button_3.button_handler(hand_results, h, w)
            button_4.button_handler(hand_results, h, w)
            button_5.button_handler(hand_results, h, w)
            button_6.button_handler(hand_results, h, w)

        cv2.imshow('Pose Estimator', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
