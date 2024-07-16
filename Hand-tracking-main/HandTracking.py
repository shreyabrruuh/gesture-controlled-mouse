import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
# capturing my video 1st video source
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime=0
cTime=0

while True:
    # loop will run forever
    success, img = cap.read()
    # reading whatever is captured
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # hands only use RGB images hence conversion important
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks) would print landmarks if hand detected else None
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm)
                # we will observe that every lm has x,y,z coordinate
                h,w,c = img.shape #height,width,channel
                cx,cy = int(lm.x*w),int(lm.y*h)
                print(id,cx,cy) # now every id will have integer coordinates of x,y,z defining pixels
                # say i want to make a circle on the tip of index finger
                # if index = 8
                # cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
                # a pink filled circle of radius 15 and center cx,cy will be displayed on id8(tip of index finger)

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS) #Hand0

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


    # process the frame for us
    cv2.imshow("Virtual Mouse", img)
    cv2.waitKey(1)

