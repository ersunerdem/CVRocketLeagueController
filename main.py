import cv2
import cvzone
import time
import handtracking
import eyetracking
import pyvjoy

def main():
    #Set up CV Capture and Detectors
    capture = cv2.VideoCapture(0)
    hand_detector = handtracking.HandDetector()
    eye_detector = eyetracking.EyeDetector(draw=False)

    #Triggers for checking blink (we don't want blink to fire for all frames where eye is closed)
    lastBlink = False
    lastLHandThumb = 0
    jumpTrigger = False
    useEyeDetector = False
    #Right Hand Control Area
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f'Setting up new capture area. Width: {int(width)}, Height: {int(height)}')
    #Center point, radius for the right-hand controller
    control_center = (480, 200)
    control_radius = 100

    #Set up PyVJoy Device, so we can control the game
    j = pyvjoy.VJoyDevice(1)

    #Run our program
    while True:
        j.data.lButtons = 0
        #Capture input
        success, img = capture.read()
        img = hand_detector.findHands(img, True, flipType=False)
        img = hand_detector.drawRightHandControlArea(img, control_center, control_radius)
        #Get individual hand control feedback
        leftHandControl, rightHandControl = hand_detector.getHandControls(img)
        #Get blink feedback
        blink = eye_detector.checkBlink(img)
        #Trigger controls
        if(useEyeDetector):
            if(blink and not lastBlink):
                jumpTrigger = True
            else:
                jumpTrigger = False
        else:
            if(leftHandControl[0] == 0 and lastLHandThumb != 0):
                jumpTrigger = True
            else:
                jumpTrigger = False

        #Set controls on PyVJoy using CV control detections
        #BUTTONS: 
        # 1 = Jump
        # 2 = Boost
        MAX_VJOY = 32767 / 2
        if(jumpTrigger):
            j.data.lButtons += 1
        if(leftHandControl == [0, 1, 1, 1, 1] or leftHandControl == [1, 1, 1, 1, 1]):
            j.data.lButtons += 2
        #Input Axis Controls
        j.data.wAxisX = int((rightHandControl[0] + 1)  * MAX_VJOY)
        j.data.wAxisY = int((rightHandControl[1] + 1) * MAX_VJOY)
        j.update()

        #Set last blink
        lastBlink = blink
        lastLHandThumb = leftHandControl[0]

        #Show text on image
        cvzone.putTextRect(img, f'Boost: {leftHandControl}', (10,20), scale=1, thickness=1, colorR=(255,0,0))
        cvzone.putTextRect(img, f'Movement Input: {rightHandControl}', (10,50), scale=1, thickness=1, colorR=(255,0,0))
        cvzone.putTextRect(img, f'Jump: {jumpTrigger}', (10,80), scale=1, thickness=1, colorR=(255,0,0))

        #Display the image from video
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()