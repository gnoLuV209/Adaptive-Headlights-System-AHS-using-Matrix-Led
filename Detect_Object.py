import cv2
import numpy as np
from time import sleep
import threading
#import serial
#_____________________________________________________________________________________________________#
# Find Mask
def Mask(roi_number):
    gray = cv2.cvtColor(roi_number, cv2.COLOR_BGR2GRAY)
    filter = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    _, thresh = cv2.threshold(filter, 220, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(thresh, 20, 200, apertureSize=3)
    return canny
#############################################################################################################
# Condition of each ROIs
def ROI1(roi_1, frame):
    mask_1 = Mask(roi_1)
    contours_1, _ = cv2.findContours(mask_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt_1 in contours_1:
        area_1 = cv2.contourArea(cnt_1)
        if  area_1 > 10:
            rect = cv2.minAreaRect(cnt_1)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.circle(roi_1, (int(x), int(y)), 3, (0, 0, 255), -1)
            cv2.polylines(roi_1, [box], True, (0, 255, 0), 2)
            cv2.putText(frame, "LOW BEAM", (40,170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2 )
            sleep(0.01)
            #arduino.write(b'1')
        else:
            cv2.putText(frame, "HIGH BEAM", (40, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#############################################################################################################
def ROI2(roi_2, frame):
    mask_2 = Mask(roi_2)
    contours_2, _ = cv2.findContours(mask_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt_2 in contours_2:
        area_2 = cv2.contourArea(cnt_2)
        if  area_2 > 10:
            rect = cv2.minAreaRect(cnt_2)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.circle(roi_2, (int(x), int(y)), 3, (0, 0, 255), -1)
            cv2.polylines(roi_2, [box], True, (0, 255, 0), 2)
            cv2.putText(frame, "LOW BEAM", (200,170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2 )
            sleep(0.01)
            #arduino.write(b'2')
        else:
            cv2.putText(frame, "HIGH BEAM", (200,170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#############################################################################################################
def ROI3(roi_3, frame):
    mask_3 = Mask(roi_3)
    contours_3, _ = cv2.findContours(mask_3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt_3 in contours_3:
        area_3 = cv2.contourArea(cnt_3)
        if  area_3 > 10:
            rect = cv2.minAreaRect(cnt_3)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.circle(roi_3, (int(x), int(y)), 3, (0, 0, 255), -1)
            cv2.polylines(roi_3, [box], True, (0, 255, 0), 2)
            cv2.putText(frame, "LOW BEAM", (360, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2 )
            sleep(0.01)
            #arduino.write(b'4')
        else:
            cv2.putText(frame, "HIGH BEAM", (360, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#############################################################################################################
def ROI4(roi_4, frame):
    mask_4 = Mask(roi_4)
    contours_4, _ = cv2.findContours(mask_4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt_4 in contours_4:
        area_4 = cv2.contourArea(cnt_4)
        if  area_4 > 10:
            rect = cv2.minAreaRect(cnt_4)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.circle(roi_4, (int(x), int(y)), 3, (0, 0, 255), -1)
            cv2.polylines(roi_4, [box], True, (0, 255, 0), 2)
            cv2.putText(frame, "LOW BEAM", (520, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
            sleep(0.01)
            #arduino.write(b'4')
        else:
            cv2.putText(frame, "HIGH BEAM", (520, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#_____________________________________________________________________________________________________#
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
    mask = Mask(roi)
    try:
        # Create 4 threads for each ROIs
        thread_1 = threading.Thread(target=ROI1, args=(roi_1, frame,))
        thread_2 = threading.Thread(target=ROI2, args=(roi_2, frame,))
        thread_3 = threading.Thread(target=ROI3, args=(roi_3, frame,))
        thread_4 = threading.Thread(target=ROI4, args=(roi_4, frame,))
        # Start 4 thread
        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()
        # Join 4 thread
        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()
        # Show value of each cases
        #print("area_1=", area_1, "area_2=", area_2, "area_3=", area_3, "area_4=", area_4)
    except:
        sleep(0.0000000001)
    cv2.rectangle(frame, (0, 0), (160, 360), (0, 0, 255), 2)
    cv2.rectangle(frame, (160, 0), (320, 360), (0, 0, 255), 2)
    cv2.rectangle(frame, (320, 0), (480, 360), (0, 0, 255), 2)
    cv2.rectangle(frame, (480, 0), (640, 360), (0, 0, 255), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
# arduino.close()
cap.release()
cv2.destroyAllWindows()
