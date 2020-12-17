#/usr/bin/env python3
from extractor import Extractor
import numpy as np
import cv2
from display import Display
w = 1920//2
h = 1080//2
F = 1
disp = Display(w,h)
K = np.array(([F,0,w//2],[0,F,h//2],[0,0,1]))
fe = Extractor(K)

def process_frame(img):
   img = cv2.resize(img,(w,h))
   matches = fe.extract(img)

   def denormalize(pt):
        return int(round(pt[0] + img.shape[0]/2)), int(round(pt[1] + img.shape[1]/2))

   for pt1,pt2 in matches:
       u1, v1 = fe.denormalize(pt1)
       u2, v2 = fe.denormalize(pt2)
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


