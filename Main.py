import cv2
from mss import mss
import numpy as np
import win32api
import serial
 
 
fov = int(input("fov: "))
 
sct = mss()
 
 
arduino = serial.Serial('COM7', 115200)
 
screenshot = sct.monitors[1]
screenshot['left'] = int((screenshot['width'] / 2) - (fov / 2))
screenshot['top'] = int((screenshot['height'] / 2) - (fov / 2))
screenshot['width'] = fov
screenshot['height'] = fov
center = fov/2
 
 
# lower = np.array([140,110,150])
# upper = np.array([150,195,255])
 
 
lower = np.array([140,111,160])
upper = np.array([148,154,194])
 
xspd = float(input("x speed...default 0.1 :"))
yspd = float(input("y speed...default 0.1 :"))
print("Ready !")
 
def mousemove(x,y):
    if x < 0: 
        x = x+256 
    if y < 0:
        y = y+256 
 
    pax = [int(x),int(y)]
    arduino.write(pax)
 
 
while True:
    if win32api.GetAsyncKeyState(0x01) < 0:
        
        img = np.array(sct.grab(screenshot))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower,upper)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations= 5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            M = cv2.moments(thresh)
            point_to_aim = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            closestX = point_to_aim[0] + 2
            closestY = point_to_aim[1] - 5
            
            diff_x = int(closestX - center)
            diff_y = int(closestY - center)
            
            target_x = diff_x * xspd
            target_y = diff_y * yspd
                
            mousemove(target_x, target_y)