import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture('Videos/VID_20210725_170617~3.mp4')

pTime = 0
detector = pm.poseDetector()
time_stand = 0
time_deitado = 0
time_sentado = 0
time_waiting = 0
x=0

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    img = cv2.resize(img, (720,720))
    lmList = detector.findPosition(img, draw=False)  # Colocar draw=False caso queira desenhar um ponto específico
    cv2.rectangle(img, (175,550), (575,675), (150, 150, 150), cv2.FILLED)
    if len(lmList) != 0:
        print(lmList[11],lmList[23], lmList[25], list(time.localtime())[5])
        #detector.findAngle(img, 11, 23, 25)

        # Desenhando um ponto específico
        #cv2.circle(img, (lmList[23][1], lmList[23][2]), 15, (255, 0, 0), cv2.FILLED)
        #cv2.circle(img, (lmList[11][1], lmList[11][2]), 15, (0, 0, 255), cv2.FILLED)
        #rcv2.circle(img, (lmList[25][1], lmList[25][2]), 15, (0, 255, 255), cv2.FILLED)

        if (lmList[11][2]*0.9) <= lmList[23][2] <= (lmList[11][2]*1.1):

            if abs(lmList[23][1] - lmList[11][1]) > 50:
                alerta = 'Pose: Lying down'
                print('alert')
                cv2.putText(img, alerta, (200, 600), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                cv2.imshow("Image", img)
                x = 'deitado'
                #time_deitado = time.time()

            elif (lmList[11][1]*0.9) <= lmList[23][1] <= (lmList[11][1]*1.1):
                pose = 'Position: Abaixando'
                print('alert')
                #cv2.putText(img, pose, (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                #cv2.imshow("Image", img)
                #x = 'abaixando'

        elif ((lmList[11][2]) <= lmList[23][2] * 0.8) and (lmList[23][2] <= (lmList[25][2]) * 0.8):
            stand = 'Pose: Standing'
            print('stand')
            cv2.putText(img, stand, (200, 600), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.imshow("Image", img)
            x = 'em pe'

            if (lmList[14][1] * 0.8) <= lmList[15][1] <= (lmList[14][1] * 1.2) and \
                    (lmList[13][1] * 0.8) <= lmList[16][1] <= (lmList[13][1] * 1.2):
                cruzado = 'PS: Arms crossed'
                cv2.putText(img, cruzado, (200, 650), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                cv2.imshow("Image", img)

        elif (((lmList[24][2]) * 0.9) <= lmList[26][2] <= ((lmList[24][2]) * 1.1)) and \
                ( (lmList[11][1])*0.9 <= lmList[23][1] <= (lmList[11][1])*1.1) and \
                (lmList[11][2] * 0.9) <= lmList[12][2] <= (lmList[11][2] * 1.1):
            sit = 'Pose: Sitting'
            print('sit')
            cv2.putText(img, sit, (200, 600), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.imshow("Image", img)
            x = 'sentado'

        else:
            unknown = 'Pose: Unknown'
            cv2.putText(img, unknown, (200, 600), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.imshow("Image", img)


    if x == 'deitado' and time_deitado == 0:
        time_stand = 0
        time_sentado = 0
        time_deitado = time.time()

    if x == 'em pe' and time_stand == 0:
        time_deitado = 0
        time_sentado = 0
        time_stand = time.time()

    if x == 'sentado' and time_sentado == 0:
        time_deitado = 0
        time_stand = 0
        time_sentado = time.time()

    # if x == 'waiting':
    #     time_deitado = 0
    #     time_stand = 0
    #     time_sentado = 0
    #     time_waiting = time.time()

    timex = time.time() - time_deitado - time_stand - time_sentado
    cv2.putText(img, f'Time: {str(int(timex))}s', (200, 625), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.imshow("Image", img)

    if timex > 5 and (x == 'deitado'):
        cv2.rectangle(img, (275, 350), (475, 415), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f'ALERT', (300, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        cv2.imshow("Image", img)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    #cv2.putText(img, f'FPS: str(int(fps))', (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    #cv2.imshow("Image", img)

    cv2.waitKey(1)

    ## https://google.github.io/mediapipe/solutions/pose.html