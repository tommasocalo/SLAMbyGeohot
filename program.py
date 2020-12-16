#/usr/bin/env python3
from extractor import Extractor
import numpy as np
import cv2
from display import Display
w = 1920//2
h = 1080//2

disp = Display(w,h)

fe = Extractor()

def process_frame(img):
   img = cv2.resize(img,(w,h))
   matches = fe.extract(img)
   for pt1,pt2 in matches:
       u1, v1 = map(lambda x : int(round(x)), pt1)
       u2, v2 = map(lambda x : int(round(x)), pt2)
       cv2.circle(img, (u1,v1), color = (0,255,0) , radius=3)
       cv2.line(img, (u1,v1),(u2,v2), color= (255,0,0))
   disp.draw(img)

if __name__ == "__main__":

    cap = cv2.VideoCapture("videos/test_countryroad.mp4")

    while cap.isOpened():
        ret, frame  = cap.read()
        if ret == True:
            process_frame(frame)
        else:
            break


