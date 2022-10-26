# Adaptive-Headlights-System-AHS-using-Matrix-Led
Design and  Simulate The Adaptive Headlights System on Automobile 
This is a personal project. Now i'll guide you how to create the model and run the code

STEP 1 : You need to prepare some electronic components
+ One Microcontroller Arduino Uno for receiving data from Small single-board computers Raspberry Pi or your personal computer and controlling the Module Matrix Led
+ Two Module Matrix Led IC MAX7219 for split the light
+ One Rheosta or steering wheel simulation
+ One Small single-board computers Raspberry Pi with Module Camera Mini Raspberry "or" your personal computer with computer's webcam for object detection
+ Two Motor Servo for controling rotation of two module Matrix Led IC MAX7219

STEP 2 : Download some sofware for this project
+ Download the Arduino IDE sofware for uploading source code to the microcontroller
+ Download the Python IDE sofware for image processing by computer vision
+ Open Command Prompt to install some package for python: type command: py -m pip install pyserial, type command: py -m pip install Pillow, type command: py -m pip install opencv-python, type command: py -m pip install pyserial

STEP 3 : Design model with all components prepared at STEP 1, you can see file "Circuit_Diagram_With2Motor.png", "Circuit_Diagram_With MatrixLedMax7219.png", "Circuit_Diagram_With_RotationSensor.png" and "DesignModel.png" for designing models

STEP 4 : Run the source code and watch the result  
+ Open Arduino IDE software and copy code in file "Control_Headlights_System.ino" to your Arduino IDE software
+ Connect to your computer and select board, here you'll chose Arduino Uno and click "upload" for loading into the microcontroller
+ Download video "VideoTest.mp4" and put in the same folder as the file "Main_Detect_Object.py "
+ Open flie "Main_Detect_Object.py " run and see the result

