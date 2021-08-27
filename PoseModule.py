import cv2
import mediapipe as mp
import time
import math

class poseDetector():

    def __init__(self, mode= False, upBody = False, smooth = True,
                 detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255,0,0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw =True):

        # pegando os valores de x e y para cada ponto do corpo
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Verificando o ângulo
        angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))
        print(angle)

        if draw:
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
            cv2.putText(img, str(int(angle)), (x2-20, y2 +50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),2)
        return angle


def main():
    #cap = cv2.VideoCapture('Videos/VID_20210612_182751.mp4')
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img,draw=False) # Colocar draw=False caso queira desenhar um ponto específico

        if len(lmList) != 0:
            print(lmList[14])

            # Desenhando um ponto específico
            cv2.circle(img, (lmList[13][1], lmList[13][2]), 15, (255, 0, 0), cv2.FILLED)

        cTime = time.time()
        fps = 1 /(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)),(70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)

        cv2.waitKey(1)

if __name__ == "__main__":
    main()