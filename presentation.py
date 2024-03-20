import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# Camera Setup
width, height = 1280, 720


# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4, height)

# get the list of presentation images
pathImages= sorted(os.listdir("Presentation"), key=len)

#Variables
imgNumber = 0
hs, ws = 120, 230
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
gestureThreshold = 450

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


while True:
    # Import Images
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join("Presentation", pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 3)

    if hands and buttonPressed==False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        cx, cy = hand['center']

        if cy<=gestureThreshold:
            print(fingers)
            # gesture 1
            if fingers[0]==1 and fingers[1]==0:
                print("left")
                print(f'cx: {cx}')
                print(f'hands: {hand["lmList"][8][0]}')
                if cx > hand['lmList'][8][0]:
                    if imgNumber > 0:
                        buttonPressed = True
                        imgNumber -= 1
            if fingers == [0, 1, 0, 0, 0]:
                print("right")
                print(f'cx: {cx}')
                print(f'hands: {hand["lmList"][8][0]}')
                if cx < hand['lmList'][8][0]:
                    # if imgNumber < len(pathImages) - 1:
                    print(imgNumber)
                    if imgNumber < len(pathImages) - 1:
                        buttonPressed = True
                        imgNumber += 1



    #button pressed iteration
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False





    # Adding webcam image on the slides
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w-ws:w] = imgSmall
    imgCurrent = cv2.resize(imgCurrent, (1500, 1000))


    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)
    key = cv2.waitKey(1)



    if key == ord('q'):
        break