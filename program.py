#/usr/bin/env python3
import cv2
from display import Display
w = 1920//2
h = 1080//2

disp = Display(w,h)

def process_frame(img):
   img = cv2.resize(img,(w,h))
   disp.draw(img)
if __name__ == "__main__":

    cap = cv2.VideoCapture("videos/test_countryroad.mp4")

    while cap.isOpened():
        ret, frame  = cap.read()
        if ret == True:
            process_frame(frame)
        else:
            break


