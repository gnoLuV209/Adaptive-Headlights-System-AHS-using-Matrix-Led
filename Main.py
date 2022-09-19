import cv2
import numpy as np
from time import sleep
#import serial
#_______________________________________________________________________#
# Detect Object
def Object_Detection(roi_number):
    gray = cv2.cvtColor(roi_number, cv2.COLOR_BGR2GRAY)
    filter = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    _, thresh = cv2.threshold(filter, 245, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(thresh, 150, 200, apertureSize=3)
    return canny
##############################################################################
# Calculate Area of Object
def Control_Light(contours_number,roi_number):
    global area_number
    for cnt_number in contours_number:
        area_number = cv2.contourArea(cnt_number)
        if area_number > 5:
            rect = cv2.minAreaRect(cnt_number)
            (x, y), _, _ = rect
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.circle(roi_number, (int(x), int(y)), 3, (0, 0, 255), -1)
            cv2.polylines(roi_number, [box], True, (0, 255, 0), 2)
    return area_number
#_______________________________________________________________________#
# Create communicate with Arduino
#arduino = serial.Serial(port='COM5', baudrate=115200, timeout=0.1)
cap = cv2.VideoCapture("VideoTest.mp4")
while True:
    _, frame = cap.read()
    # Extract Region of interest
    roi = frame[190:340, :]
    roi_1 = frame[190:340, 0:160]
    roi_2 = frame[190:340, 161:320]
    roi_3 = frame[190:340, 321:480]
    roi_4 = frame[190:340, 481:640]
    #  Mask
    mask = Object_Detection(roi)
    try:
        # Detect Roi_1
        mask_1 = Object_Detection(roi_1)
        contours_1, _ = cv2.findContours(mask_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area_1 = 0
        area_1 = area_1 + Control_Light(contours_1, roi_1)
        if  area_1 > 5:
            cv2.putText(frame, "LOW BEAM", (40,170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2 )
            sleep(0.01)
            #arduino.write(b'1')
        else :
            cv2.putText(frame, "HIGH BEAM", (40, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # Detect Roi_2
        mask_2 = Object_Detection(roi_2)
        contours_2, _ = cv2.findContours(mask_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area_2 = 0
        area_2 = area_2 + Control_Light(contours_2, roi_2)
        if  area_2 > 5:
            cv2.putText(frame, "LOW BEAM", (200,170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2 )
            sleep(0.01)
            #arduino.write(b'2')
        else:
            cv2.putText(frame, "HIGH BEAM", (200, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            sleep(0.1)
        # Detect Roi_3
        mask_3 = Object_Detection(roi_3)
        contours_3, _ = cv2.findContours(mask_3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area_3 = 0
        area_3 = area_3 + Control_Light(contours_3, roi_3)
        if area_3 > 5:
            cv2.putText(frame, "LOW BEAM", (360, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2 )
            sleep(0.01)
            #arduino.write(b'3')
        else:
            cv2.putText(frame, "HIGH BEAM", (360, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # Detect Roi_4
        mask_4 = Object_Detection(roi_4)
        contours_4, _ = cv2.findContours(mask_4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        area_4 = 0
        area_4 = area_4 + Control_Light(contours_4, roi_4)
        if area_4 > 5:
            cv2.putText(frame, "LOW BEAM", (520, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2 )
            sleep(0.01)
            #arduino.write(b'4')
        else:
            cv2.putText(frame, "HIGH BEAM", (520, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # Show value of each cases
        print("area_1=", area_1, "area_2=", area_2, "area_3=", area_3, "area_4=", area_4)
    except:
        sleep(0.0000000001)
    cv2.rectangle(frame, (0, 0), (160, 360), (0, 0, 255), 2)
    cv2.rectangle(frame, (160, 0), (320, 360), (0, 0, 255), 2)
    cv2.rectangle(frame, (320, 0), (480, 360), (0, 0, 255), 2)
    cv2.rectangle(frame, (480, 0), (640, 360), (0, 0, 255), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# arduino.close()
cap.release()
cv2.destroyAllWindows()
