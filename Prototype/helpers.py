# helpers.py
# functions to help other files
import cv2

def getRGBOfImage(image_path):
	img = cv2.imread(image_path)

	total_blue = 0
	total_green = 0
	total_red = 0
	for i in range(0, len(img)):
			for j in range(0, len(img[i])):
					total_blue += img[i,j][0]
					total_green += img[i,j][1]
					total_red += img[i,j][2]

	b = total_blue / (len(img) * len(img))
	g = total_green / (len(img) * len(img))
	r = total_red / (len(img) * len(img))

	return r,g,b

