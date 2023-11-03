import os.path
import time

import cv2

IMAGE_PATH = "./train/"

label = "left_pointer"
image_num = 40

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

for ind in range(image_num):
    res, frame = cap.read()
    image_name = os.path.join(IMAGE_PATH, label, str(round(time.time()*1000)) + label + ".jpg")
    cv2.imwrite(image_name, frame)
    cv2.imshow('frame', frame)
    time.sleep(1)
    print("capture")

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
cap.release()
