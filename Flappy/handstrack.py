import math
import cv2
import mediapipe as mp
from screeninfo import get_monitors
for m in get_monitors():
    win_width = m.width
    win_height = m.height

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
if not cap.isOpened():
  cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    static_image_mode=False,
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    ret, frame = image.read()
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    frame = cv2.resize(image,(450,450))

    frame_width, frame_height = frame.shape[1], frame.shape[0]
    frame_x = win_width - frame_width
    frame_y = win_height - frame_height

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', frame)
    cv2.moveWindow('MediaPipe Hands',frame_x,frame_y)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()