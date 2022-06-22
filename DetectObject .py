import cv2
import numpy as np
import serial



# Detect Object
def Object_Detection(roi_number):
    detect = cv2.cvtColor(roi_number, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5,5), np.uint8)
    detect = cv2.erode(detect, kernel, iterations=1) 
    detect = cv2.dilate(detect, kernel, iterations=1)
    detect = cv2.GaussianBlur(detect, (5,5), 0)
    detect = cv2.morphologyEx(detect, cv2.MORPH_CLOSE, kernel)
    _, detect = cv2.threshold(detect, 175, 255, cv2.THRESH_BINARY)
    detect = cv2.Canny(detect,50,150)
    return detect

# Calculate Area of Object
def Control_Light(contours_number,area_number):
    for cnt_number in contours_number:
        area_number = cv2.contourArea(cnt_number)+area_number
    return area_number


# Create comunicate with Arduino
#arduino = serial.Serial(port='COM9', baudrate=115200, timeout=0.1)
cap = cv2.VideoCapture("test2.mp4")

while True:
    _, frame = cap.read() 
    # Extract Region of interest
    roi   = frame[150:360,:]
    roi_1 = frame[:,0:160]
    roi_2 = frame[:,161:320]
    roi_3 = frame[:,321:480]
    roi_4 = frame[:,481:640]
    #  Object Detection
    mask    = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    kernel  = np.ones((5,5), np.uint8)
    mask    = cv2.erode(mask, kernel, iterations=1) 
    mask    = cv2.dilate(mask, kernel, iterations=1)
    mask    = cv2.GaussianBlur(mask, (5,5), 0)
    mask    = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    _, mask = cv2.threshold(mask, 175, 255, cv2.THRESH_BINARY)
    mask    = cv2.Canny(mask,50,150)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.circle(roi, (int(x), int(y)), 3, (0, 0, 255), -1)
            cv2.polylines(roi, [box], True, (0, 255, 0), 2)
            #cv2.rectangle(roi,(int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 3)
    # Detect Roi_1         
    mask_1 = Object_Detection(roi_1)
    contours_1, _ = cv2.findContours(mask_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area_1 = 0
    area_1 = Control_Light(contours_1,area_1)
    # Detect Roi_2         
    mask_2 = Object_Detection(roi_2)
    contours_2, _ = cv2.findContours(mask_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area_2 = 0
    area_2 = Control_Light(contours_2,area_2)
    # Detect Roi_3         
    mask_3 = Object_Detection(roi_3)
    contours_3, _ = cv2.findContours(mask_3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area_3 = 0
    area_3 = Control_Light(contours_3,area_3)
    # Detect Roi_4         
    mask_4 = Object_Detection(roi_4)
    contours_4, _ = cv2.findContours(mask_4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area_4 = 0
    area_4 = Control_Light(contours_4,area_4)
    
    # Condtion of each cases
    if area_1 > 100:
        print(1)
        #arduino.write(b'1')  
    elif area_2 > 100:
        print(2)
        #arduino.write(b'2')    
    elif area_3 > 100:
        print(3)
        #arduino.write(b'3')   
    elif area_4 > 100:
        print(4)
        #arduino.write(b'4')   
    elif area_1 < 100 and area_2 < 100 and area_3 < 100 and area_4 < 100 :
        print(0)
        #arduino.write(b'0')
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    

    if cv2.waitKey(10) & 0xFF == ord('q'):
         break

#arduino.close()
cap.release()
cv2.destroyAllWindows()
