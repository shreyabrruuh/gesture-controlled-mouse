import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0) #first video source captured
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
while True:
    r, frame = cap.read()
    frame = cv2.flip(frame, 1) #flip frame on y axis(1) since video is mirror image so fixed
    frame_height, frame_width, frame_channel = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #detecting hands best done in rgb mode
    output = hand_detector.process(rgb_frame)
    #processing the hands
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            # hands is landmark
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                print(x,y) #x and y are integer coordinates

                #identify index finger
                if id == 8: #index finger is selected
                    cv2.circle(img=frame, center=(x, y), radius=20, color=(255, 0, 255), thickness=-1)

                    # these calculations need to be done so that finger moves on whole screen and not limited to frame
                    # moving the finger as cursor
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y


                if id==4: #thumb is selected
                    cv2.circle(img=frame, center=(x, y), radius=20, color=(255, 0, 255), thickness=-1)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('outside',abs(index_y - thumb_y))
                    pyautogui.moveTo(index_x, index_y)
                #if the y distance between thumb and finger decreases enable click
                    if abs(index_y - thumb_y) < 30:
                        print('click')
                        pyautogui.click()
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)

                         # enables click functionality

    cv2.imshow("Virtual Mouse", frame)
    cv2.waitKey(1)



























#refer: https://www.youtube.com/watch?v=vJWzH_2F64g&list=TLPQMDcwMzIwMjMgV5BRtnwYWg&index=1