#/usr/bin/env python3
import g2o
from frame import Frame,denormalize,match
import numpy as np
import cv2
from display import Display


w = 1920//2
h = 1080//2
F = 270
K = np.array(([F,0,w//2],[0,F,h//2],[0,0,1]))

disp = Display(w,h)

frames = []
def process_frame(img):
   img = cv2.resize(img,(w,h))
   frame = Frame(img, K)
   frames.append(frame)
   if len(frames) <= 1:
       return

   ret, Rt = match(frames[-1], frames[-2])
   for pt1,pt2 in ret:
       u1, v1 = denormalize(K,pt1)
       u2, v2 = denormalize(K,pt2)
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


