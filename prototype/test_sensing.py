"""@module test_sensing
Test the sensing module on example images of known values.

Author: Josh Rands
Date: 2/5/2020 
Email: joshrands1@gmail.com
"""

import colorsys
import matplotlib.pyplot as plt

import logging as log
from sensing import get_img, get_average_rgb_from_img, get_scale_map, get_distance_between_points_3d
import init 

if __name__ == '__main__':

    arg_vals = init.get_args()

    init.init(arg_vals['verbose'])

    ### TEST PH ###
    test_imgs = {'6,8-test.png':6.8,
                 '6,8-test2.png':6.8,
                 '7,2-test.png':7.2,
                 '7,8-test.png':7.8,
                 '8,2-test.png':8.2}

    for img_key in test_imgs.keys():
        img = get_img('file', img_key)

        r,g,b = get_average_rgb_from_img(img)

        scale = get_scale_map('pH')

        # Try with HSV 
        h,s,v = colorsys.rgb_to_hsv(r,g,b)

        hsv_scale = {}

        # get the distance from each point in the scale 
        closest = 255
        closest_key = ""

        hsv_closest = 255
        hsv_key = ""

        hue = []
        ph = []

        for key in scale:
            rgb = scale[key]
            dist = get_distance_between_points_3d(rgb, [r,g,b])

            # populate hsv scale
            new_rgb = [val * 255 for val in rgb]
            print(new_rgb)
            hsv_scale[key] = colorsys.rgb_to_hsv(*new_rgb)

            if dist < closest:
                closest = dist
                closest_key = key

            hsv = hsv_scale[key]
            hsv_dist = abs(hsv[0] - h)
            if hsv_dist < hsv_closest:
                hsv_closest = hsv_dist
                hsv_key = key

            hue.append(hsv[0])
            ph.append(float(key))
            print(hsv[0])
            print(rgb)

        print("RGB: " + str(test_imgs[img_key]) + " = " + closest_key)
        print("Hue: " + str(test_imgs[img_key]) + " = " + hsv_key)

        hue.append(h)
        ph.append(float(hsv_key))

        # plot hue graph 
        plt.scatter(ph, hue)
        plt.show()
