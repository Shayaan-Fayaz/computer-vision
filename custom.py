import cv2
from cvzone.HandTrackingModule import HandDetector
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


# list of presentation images
folderPath = 'Presentation'
pathImages = sorted(os.listdir(folderPath), key=len)


# variables
imgNumber = 0
hs, ws = 120, 213
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30

detecor = HandDetector(detectionCon=0.5, maxHands=1)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detecor.findHands(img)
    cv2.line(img, (0, gestureThreshold), (1280, gestureThreshold), (0, 255, 0), 10)


    if hands and buttonPressed==False:
        hand = hands[0]
        fingers = detecor.fingersUp(hand)
        cx, cy = hand['center']
        lmlist = hand['lmList']
        indexFinger = lmlist[8][0]
        middleFinger = lmlist[12][0]

        if cy<=gestureThreshold:
            if fingers == [0, 1, 1, 0, 0]:
                if middleFinger > indexFinger:
                    if imgNumber < len(pathImages) - 1:
                        buttonPressed=True
                        imgNumber+=1

                if middleFinger<indexFinger:
                    if imgNumber > 0:
                        buttonPressed=True
                        imgNumber -= 1

        if buttonPressed:
            buttonCounter += 1
            if buttonCounter > buttonDelay:
                counter = 0
                buttonPressed = False

        cv2.imshow("Image", img)
        cv2.imshow("Slides", imgCurrent)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break



        print(f'Index finger: {indexFinger}, Middle Finger: {middleFinger}')
        # print(middleFinger)



    # cv2.imshow("Images", imgCurrent)
    # key = cv2.waitKey(1)


