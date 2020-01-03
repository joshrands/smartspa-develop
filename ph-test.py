import cv2 
import numpy as np
print(cv2.__version__)

ph_start = 6.4
ph_end = 7.2

# classify each ph reading as RGB value  

img = cv2.imread('pH-colors/6_4.png')

total_blue = 0
total_green = 0
total_red = 0
for i in range(0, len(img)):
    for j in range(0, len(img[i])):
#        print(img[i,j])
#        print(img[i,j][0])
        total_blue += img[i,j][0]
        total_green += img[i,j][1]
        total_red += img[i,j][2]

min_blue = total_blue / (len(img) * len(img))
min_green = total_green / (len(img) * len(img))
min_red = total_red / (len(img) * len(img))

print(min_red, min_green, min_blue)

img = cv2.imread('pH-colors/7_2.png')

total_blue = 0
total_green = 0
total_red = 0
for i in range(0, len(img)):
    for j in range(0, len(img[i])):
#        print(img[i,j])
#        print(img[i,j][0])
        total_blue += img[i,j][0]
        total_green += img[i,j][1]
        total_red += img[i,j][2]

max_blue = total_blue / (len(img) * len(img))
max_green = total_green / (len(img) * len(img))
max_red = total_red / (len(img) * len(img))

print(max_red, max_green, max_blue)

img_name = "6_8.png"# raw_input("Enter new image path or 'q' to quit: ")

delta_red = float(max_red - min_red)
delta_green = float(max_green - min_green)
delta_blue = float(max_blue - min_blue)
print("Deltas", delta_red, delta_green, delta_blue)
total_delta = (delta_red) + (delta_green) + (delta_blue)

# weigh each color from delta 
red_weight = abs(float(delta_red / total_delta))
green_weight = abs(float(delta_green / total_delta))
blue_weight = abs(float(delta_blue / total_delta))
print(red_weight, green_weight, blue_weight)

ph_range = ph_end - ph_start

while (img_name != "q"):
    print(img_name)

    img = cv2.imread("pH-colors/" + img_name)

    total_blue = 0
    total_green = 0
    total_red = 0
    for i in range(0, len(img)):
        for j in range(0, len(img[i])):
    #        print(img[i,j])
    #        print(img[i,j][0])
            total_blue += img[i,j][0]
            total_green += img[i,j][1]
            total_red += img[i,j][2]

    blue = total_blue / (len(img) * len(img))
    green = total_green / (len(img) * len(img))
    red = total_red / (len(img) * len(img))

    print(red, green, blue)

    # classify the pH
    dif_red = (max_red - red)
    dif_green = (max_green - green)
    dif_blue = (max_blue - blue)
    print("Diffs", dif_red, dif_green, dif_blue)

    delta_ph = dif_red * red_weight + dif_green * green_weight + dif_blue * blue_weight
    print("pH = " + str(ph_end + delta_ph))

    img_name = raw_input("Enter new image path or 'q' to quit: ")


