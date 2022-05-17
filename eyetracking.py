#Followed Murtaza Hassan's Eye Blink Counter using OpenCV Python Video, modified the code a bit: https://www.youtube.com/watch?v=-TVUwH1PgBs

import cv2
from cvzone.FaceMeshModule import FaceMeshDetector


class EyeDetector():
    def __init__(self, maxFaces=1, draw=True):
        self.maxFaces = maxFaces
        self.draw = draw
        self.detector = FaceMeshDetector()
        self.ratioList = []

    def checkBlink(self, img):
        ids = [22,23,24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
        img, faces = self.detector.findFaceMesh(img, draw=self.draw)
        if(len(faces) > 0):
            face = faces[0]
            for id in ids:
                cv2.circle(img, face[id], 2,(255,0,255), cv2.FILLED)
            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            len_vertical, _ = self.detector.findDistance(leftUp, leftDown)
            len_horizontal, _ = self.detector.findDistance(leftLeft, leftRight)
            len_ratio = int((len_vertical / len_horizontal) * 100)
            self.ratioList.append(len_ratio)
            if(len(self.ratioList) > 3):
                self.ratioList.pop(0)
            ratioAvg = sum(self.ratioList) / len(self.ratioList)

            #print(len_ratio)
            cv2.line(img, leftUp, leftDown, (0,200,0), 1)
            cv2.line(img, leftLeft, leftRight, (0,200,0), 1)
            if(ratioAvg < 36):
                return True
            else:
                return False
        return False
