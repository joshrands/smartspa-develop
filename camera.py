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

#cv2.imwrite('frame.png',frame)

cap.release()

img = cv2.imread('frame.png')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#ret, thresh = cv2.threshold(gray,190,255,cv2.THRESH_BINARY_INV)

total_blue = 0
total_green = 0
total_red = 0
for i in range(0, len(img)):
    for j in range(0, len(img)):
#        print(img[i,j])
#        print(img[i,j][0])
        total_blue += img[i,j][0]
        total_green += img[i,j][1]
        total_red += img[i,j][2]

print(total_blue, total_green, total_red)
blue = total_blue / (len(img) * len(img))
green = total_green / (len(img) * len(img))
red = total_red / (len(img) * len(img))

print(red, green, blue)
#print(blue, green, red)

#contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#print(len(countours))

#for i in range(0,len(contours)):
#    M = cv2.moments(contours[i])
#    cx = int(M['m10']/M['m00'])
#    cy = int(M['m01']/M['m00'])
#    print "Centroid = ", cx, ", ", cy
#    center_px = np.array([4,3,2],dtype=np.uint8)
#
#    center_px = img[cx,cy]
#    print(center_px)

