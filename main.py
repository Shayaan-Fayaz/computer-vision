import os
from cvzone.HandTrackingModule import HandDetector
import cv2

width, height = 1280, 720
folderPath = "Presentation"

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get the list of presentation images

pathImages = sorted(os.listdir(folderPath), key=len)

#variables
imgNumber = 0
hs, ws = 120, 213
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30

detector = HandDetector(detectionCon=0.5, maxHands=1)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed==False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        indexFinger = lmList[8][0:2]

        if cy<=gestureThreshold:
            # gesture 1: Left
            if fingers == [1, 0, 0, 0, 0]:
                print('Left')
                if imgNumber > 0:
                    buttonPressed=True
                    imgNumber -= 1

            #gesture 2: right
            if fingers == [0, 0, 0, 0, 1]:
                print('Right')
                if imgNumber < len(pathImages) - 1:
                    buttonPressed=True
                    imgNumber += 1

        # gesture 3: Show pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if buttonPressed:
            buttonCounter += 1
            if buttonCounter > buttonDelay:
                counter = 0
                buttonPressed = False

        cv2.imshow("Slides", imgCurrent)
        cv2.imshow("Image", img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break