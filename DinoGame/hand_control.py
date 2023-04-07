import mediapipe as mp
import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector
from screeninfo import get_monitors

for m in get_monitors():
    win_width = m.width
    win_height = m.height

def initializer():
    

    video = cv2.VideoCapture(0)
    if not video.isOpened():
        video = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.7,maxHands=1)

    return video, detector

detector = HandDetector(detectionCon=0.7,maxHands=1)

def get_label_hand(kill_check,video,detector):

    return_label = ""
    jump=[1,1,1,1,1]
    dirn = [1,0,0,0,0]
    duck= [0,1,0,0,0]
    checker = True
    while checker:
        

        ret, frame = video.read()
        # if not ret:
        #     ret, frame  = video.read()
        frame = cv2.resize(frame, (450, 450))
        hands, image = detector.findHands(frame)
        frame.flags.writeable = False
        # Get window dimensions
        # win_width, win_height = 800, 600

        # Calculate frame position
        frame_width, frame_height = frame.shape[1], frame.shape[0]
        frame_x = win_width - frame_width
        frame_y = win_height - frame_height
        if kill_check=="kill_int":
            checker=False
        if hands:
            lmList = hands[0]
            fingerUp = detector.fingersUp(lmList)
            check_type = lmList['type']
            # print(type(lmList['type']))
            # print(type(fingerUp))
            if check_type=="Left" and fingerUp==dirn:
                # print("Inside if")
                return_label = "right"
                cv2.imshow("Frame", frame)
                cv2.moveWindow("Frame", frame_x, frame_y)
                key=cv2.waitKey(1)
                if key==ord('q'):
                    break
                # video.release()
                # cv2.destroyAllWindows()
      
                return return_label
            elif check_type=="Right" and fingerUp==dirn:
                # print("Inside if")
                return_label = "left"
                cv2.imshow("Frame", frame)
                cv2.moveWindow("Frame", frame_x, frame_y)
                key=cv2.waitKey(1)
                if key==ord('q'):
                    break
                # video.release()
                # cv2.destroyAllWindows()
                return return_label
            elif fingerUp == jump and (check_type=="Right" or check_type=="Left"):
                # print("Inside if")
                return_label = "jump" 
                cv2.imshow("Frame", frame)
                cv2.moveWindow("Frame", frame_x, frame_y)
                key=cv2.waitKey(1)
                if key==ord('q'):
                    break
                # video.release()
                # cv2.destroyAllWindows()
                return return_label
            elif fingerUp ==duck and (check_type=="Right" or check_type=="Left"):
                return_label = "duck" 
                cv2.imshow("Frame", frame)
                cv2.moveWindow("Frame", frame_x, frame_y)
                key=cv2.waitKey(1)
                if key==ord('q'):
                    break
                return return_label
            else:
                return_label="no_input"
                cv2.imshow("Frame", frame)
                cv2.moveWindow("Frame", frame_x, frame_y)
                key=cv2.waitKey(1)
                if key==ord('q'):
                    break
        # print(return_label)
                return return_label
            
            
        cv2.imshow("Frame", frame)
        cv2.moveWindow("Frame", frame_x, frame_y)
        key=cv2.waitKey(1)
        if key==ord('q'):
            break

    
    video.release()
    cv2.destroyAllWindows()
    
    return return_label

def kill_feed(video):
    video.release()
    cv2.destroyAllWindows()