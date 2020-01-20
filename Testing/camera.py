import cv2 
import numpy as np
print(cv2.__version__)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

while True:
    cv2.imshow('img1', frame)
    if (cv2.waitKey(1) & 0xFF == ord('y')):
        cv2.imwrite('frame.png',frame)
        cv2.destroyAllWindows()
        break

cap.release()

