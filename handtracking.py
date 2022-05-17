#Modified code after following along Murtaza Hassan's freeCodeCamp.org course video: https://www.youtube.com/watch?v=01sAkU_NvOY

from turtle import right
import cv2
import mediapipe as mp
import math
from cvzone.HandTrackingModule import HandDetector as hd

class HandDetector():
    def __init__(self, static_image_mode = False, max_num_hands = 2, min_detection_confidence = 0.5, min_tracking_confidence = 0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.detector = hd(detectionCon=0.8, maxHands=2)


    def findHands(self, img, draw=True, flipType=False):
        self.hands, img = self.detector.findHands(img, draw, flipType)
        return img
    
    def drawRightHandControlArea(self, img, control_center, control_radius):
        #Draw Input Center and Control Circle
        self.control_center = control_center
        self.control_radius = control_radius
        #Center
        cv2.circle(img, self.control_center, 10, (0,0,255), cv2.FILLED)
        #Control Circle
        cv2.circle(img, self.control_center, self.control_radius, (255, 255, 0))
        return img

    #Returns a tuple, [x,y] where x = [-1,1] and y = [-1,1]
    def getRightHandControls(self, hand, img):
        #Right Hand controls only (movement axis)
        handPoints = [0,1,9, 13]
        px = []
        py = []
        control_x = 0
        control_y = 0


        if(len(hand) > 0):
            for id in handPoints:
                px.append(hand["lmList"][id][0])
                py.append(hand["lmList"][id][1])
        
        if(len(px) > 0):
            centerPoint = int(sum(px)/len(px)), int(sum(py)/len(py))
            #print(centerPoint)
            
            
            #Get difference in point position
            control_x = centerPoint[0] - self.control_center[0]
            control_y = centerPoint[1] - self.control_center[1]
        
            #If absolute value of distance (hypotenuse) is greater than 1, set equal to 1
            dist = abs(math.hypot(control_x, control_y) / self.control_radius)
            input = 0, 0
            theta = 0
            if(control_x == 0):
                if(control_y < 0):
                    theta = math.pi / 2
                else:
                    theta = 3 * math.pi / 2
            else:
                #atan ranges between -pi/2 and pi/2
                theta = math.atan(control_y / control_x)
                if(control_x < 0):
                    theta -= math.pi

            if(dist >= 1):
                input = round(math.cos(theta),2), round(math.sin(theta),2)
            else:
                input = round(dist * math.cos(theta),2), round(dist * math.sin(theta),2)

            cv2.line(img, self.control_center, centerPoint, (255,255,255), 1)
            cv2.circle(img, centerPoint, 10,(255 * abs(dist),0, 255 * (1 - abs(dist))), cv2.FILLED)
            
        
        
        return input
    

    def getLeftHandControls(self, hand):
        #Left Hand controls only (boost/no boost)
        return self.detector.fingersUp(hand)

    def getHandControls(self, img):
        leftControl = [0, 0, 0, 0, 0]
        rightControl = [0,0]
        if self.hands:
            for hand_id in range(len(self.hands)):
                hand = self.hands[hand_id]
                if hand["type"] == "Left":
                    leftControl = self.getLeftHandControls(hand)
                else:
                    rightControl = self.getRightHandControls(hand, img)
        return [leftControl, rightControl]
