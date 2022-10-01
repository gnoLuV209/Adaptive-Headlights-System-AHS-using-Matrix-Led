import cv2
import numpy as np
from time import sleep
import threading
import serial
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
def ROI_left(roi_left, frame, data):
    mask_left = Mask(roi_left)
    contours_left, _ = cv2.findContours(mask_left, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours_left is not None:
        for cnt_l in contours_left:
            area_l = cv2.contourArea(cnt_l)
            if  area_l > 30:
                rect = cv2.minAreaRect(cnt_l)
                (x, y), (w, h), angle = rect
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.circle(roi_left, (int(x), int(y)), 3, (0, 0, 255), -1)
                cv2.polylines(roi_left, [box], True, (0, 255, 0), 2)
                cv2.putText(frame, "LOW BEAM", (30,170), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0),2 )
                try:
                    arduino.write(b'left')
                    sleep(0.01)
                except:
                    sleep(0.0001)
        if data == 'high_left and high_right' or data == 'high_left and high_mid':
            cv2.putText(frame, "HIGH BEAM", (30,170), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0),2 )
#############################################################################################################
def ROI_mid(roi_mid, frame, data):
    mask_mid = Mask(roi_mid)
    contours_mid, _ = cv2.findContours(mask_mid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours_mid is not None:
        for cnt_m in contours_mid:
            area_m = cv2.contourArea(cnt_m)
            if  area_m > 30:
                rect = cv2.minAreaRect(cnt_m)
                (x, y), (w, h), angle = rect
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.circle(roi_mid, (int(x), int(y)), 3, (0, 0, 255), -1)
                cv2.polylines(roi_mid, [box], True, (0, 255, 0), 2)
                cv2.putText(frame, "LOW BEAM", (260,170), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0),2 )
                try:
                    arduino.write(b'mid')
                    sleep(0.01)
                except:
                    sleep(0.0001)
        if data == 'high_mid and high_right' or data == 'high_left and high_mid':
            cv2.putText(frame, "HIGH BEAM", (260,170), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0),2 )
#############################################################################################################
def ROI_right(roi_right, frame, data):
    mask_right = Mask(roi_right)
    contours_right, _ = cv2.findContours(mask_right, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours_right is not None:
        for cnt_r in contours_right:
            area_r = cv2.contourArea(cnt_r)
            if  area_r > 30:
                rect = cv2.minAreaRect(cnt_r)
                (x, y), (w, h), angle = rect
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.circle(roi_right, (int(x), int(y)), 3, (0, 0, 255), -1)
                cv2.polylines(roi_right, [box], True, (0, 255, 0), 2)
                cv2.putText(frame, "LOW BEAM", (510, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0), 2)
                try:
                    arduino.write(b'right')
                    sleep(0.01)
                except:
                    sleep(0.0001)
        if data == 'high_left and high_right' or data == 'high_mid and high_right':
            cv2.putText(frame, "HIGH BEAM", (510,170), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0),2 )
#_____________________________________________________________________________________________________#
# Create communicate with Arduino
arduino = serial.Serial(port='COM9', baudrate=115200, timeout=0.1) 
cap = cv2.VideoCapture("VideoTest.mp4")
while True:
    _, frame = cap.read()
    # Extract Region of interest
    roi = frame[190:340, :]
    roi_left = frame[190:340, 0:160]
    roi_mid = frame[190:340, 161:480]
    roi_right = frame[190:340, 481:640]
    #  Mask
    mask = Mask(roi)
    signal_high = arduino.readline()
    data = signal_high.decode('utf-8')
    data = data.rstrip()
    #print(data)
    try:
        # Create 3 threads for each ROIs
        thread_left = threading.Thread(target=ROI_left, args=(roi_left, frame, data,))
        thread_mid = threading.Thread(target=ROI_mid, args=(roi_mid, frame, data,))
        thread_right = threading.Thread(target=ROI_right, args=(roi_right, frame, data,))
        # Start 3 thread
        thread_left.start()
        thread_mid.start()
        thread_right.start()
        # Join 3 thread
        thread_left.join()
        thread_mid.join()
        thread_right.join()
    except:
        sleep(0.0000000001)
    cv2.rectangle(frame, (0, 0), (160, 360), (0, 0, 255), 2)
    cv2.rectangle(frame, (160, 0), (480, 360), (0, 0, 255), 2)
    cv2.rectangle(frame, (480, 0), (640, 360), (0, 0, 255), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
arduino.close()
cap.release()
cv2.destroyAllWindows()
