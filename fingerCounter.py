import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

while True:
    success, img = cap.read()

    hands, img = detector.findHands(img, draw=True, flipType=True)

    totalFingers = 0

    # cvzone.putTextRect(img, f"{totalFingers}", (50, 50), scale=3, thickness=3, colorT=(255, 255,255), colorR=(255, 0, 255), font=cv2.FONT_HERSHEY_PLAIN, offset=50, border=None, colorB=(0, 255, 0))

    # cvzone.putTextRect()

    if hands:
        for hand in hands:
            totalFingers += sum(detector.fingersUp(hand))
            cvzone.putTextRect(img, f"Count: {totalFingers}", pos=(100, 100), scale=3, thickness=3, colorT=(255, 255, 255), colorR=(255, 0, 255), font=cv2.FONT_HERSHEY_PLAIN, offset=50, border=None, colorB=(0, 255, 0))

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        center1 = hand1["center"]
        handType1 = hand1["type"]

        fingers1 = detector.fingersUp(hand1)
        print(f'H1 = {fingers1.count(1)}', end=" ")

        totalFingers = fingers1


        tipOfIndexFinger = lmList1[8][0:2]
        tipOfThumbFinger = lmList1[4][0:2]

        length, info, img = detector.findDistance(tipOfIndexFinger, tipOfThumbFinger, img, color=(255, 0, 255),
                                                 scale=5)

        if len(hands) == 2:
            # Information for the second hand
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            # Count the number of fingers up for the second hand
            fingers2 = detector.fingersUp(hand2)
            print(f'H2 = {fingers2.count(1)}', end=" ")
            tipOfIndexFinger2 = lmList2[8][0:2]
            tipOfThumbFinger2 = lmList2[4][0:2]
            # Calculate distance between the index fingers of both hands and draw it on the image
            length, info, img = detector.findDistance(tipOfThumbFinger2, tipOfIndexFinger2, img, color=(255, 0, 0),
                                                      scale=10)


        print(" ")

    cv2.imshow("Hand Tracking Module", img);
    cv2.waitKey(1)