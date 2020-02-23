"""@module test_sensing
Test the sensing module on example images of known values.

Author: Josh Rands
Date: 2/5/2020 
Email: joshrands1@gmail.com
"""

import colorsys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import io 
import numpy as np

import logging as log
from sensing import get_img, get_average_rgb_from_img, get_scale_map, get_distance_between_points_3d
import init 


def interpolate_rgb_values(chemical, value):
    scale = get_scale_map(chemical)

    # find closest two
    count = 0

    low_value = 0
    high_value = 9999999

    for key in scale:
        dif = value - float(key)

        print(float(key))

        if dif == 0:
            # return rgb values 
            print
            return [value,scale[key]], [value,scale[key]], [value,scale[key]]
        elif dif > 0 and float(key) > low_value:
            low_value = float(key)
#            print("Low: " + str(low_value))
        elif dif < 0 and float(key) < high_value:
            high_value = float(key)
#            print("High: " + str(high_value))

    print(str(value) + " between " + str(low_value) + " and " + str(high_value)) 

    # interpolate rgb values 
    ratio = (float(value) - low_value) / (float(high_value) - float(low_value))
    inter_r = float(255 * scale[str(low_value)][0] + (scale[str(high_value)][0] - scale[str(low_value)][0]) * ratio * 255) / 255.0
    inter_g = float(255 * scale[str(low_value)][1] + (scale[str(high_value)][1] - scale[str(low_value)][1]) * ratio * 255) / 255.0 
    inter_b = float(255 * scale[str(low_value)][2] + (scale[str(high_value)][2] - scale[str(low_value)][2]) * ratio * 255) / 255.0 

    print(inter_r, inter_g, inter_b)

    low_rgb = scale[str(low_value)]# [float(255*val) for val in scale[str(low_value)]]
    high_rgb = scale[str(high_value)] # [float(255*val) for val in scale[str(high_value)]]

    print(low_rgb)
    print(high_rgb)

    return [value,[inter_r, inter_g, inter_b]], [low_value,low_rgb], [high_value,high_rgb]


def create_interpolated_rgb_graph(chemical, increments=10, labels=False):
    scale = get_scale_map(chemical)

    red = []
    green = []
    blue = []
    values = []

    # 3D Plot
    fig = plt.figure()
    ax = Axes3D(fig)

    # turn keys into floats to sort 
    keys = sorted([float(val) for val in list(scale.keys())])
    # turn keys back into strings 
    keys = [str(val) for val in keys]
    previous_key = None 
    print(keys)
    print(scale.keys())
    for key in keys: 
        # interpolate increments amount towards next key 

        if len(red) > 0:
            inc_size = (float(key) - float(previous_key)) / float(increments)
            for i in range(1,increments):
                print("Interpolating " + str(float(previous_key) + inc_size * i))
                actual,low,high = interpolate_rgb_values(chemical, float(previous_key) + inc_size * i)
                red.append(actual[1][0])
                green.append(actual[1][1])
                blue.append(actual[1][2])
                if labels:
                    ax.text(red[-1],green[-1],blue[-1],str(float(previous_key) + inc_size * i))

        if key == '0.0':
            key = '0'
        red.append(scale[key][0])
        green.append(scale[key][1])
        blue.append(scale[key][2])
        ax.text(red[-1],green[-1],blue[-1],key)

        previous_key = key

    ax.scatter(red,green,blue)

    ax.set_title(chemical + '_rgb_3d')
    ax.set_xlabel("Red")
    ax.set_ylabel("Green")
    ax.set_zlabel("Blue")

    plt.savefig('./research/' + chemical + '/rgb_interpolated_3d.png')
    plt.show()


def create_scale_hue_graph(chemical):
    scale = get_scale_map(chemical)

    hues = []
    sat = []
    val = []
    red = []
    green = []
    blue = []
    values = []

    # 3D Plot
    fig = plt.figure()
    ax = Axes3D(fig)

    for key in scale:
        values.append(float(key))

        h,s,v = colorsys.rgb_to_hsv(*(scale[key]))
        hues.append(h)
        sat.append(s)
        val.append(v)

        ax.text(hues[-1],sat[-1],val[-1],str(key))

    ax.scatter(hues,sat,val)

    ax.set_title(chemical + '_hsv_3d')
    ax.set_xlabel("Hue")
    ax.set_ylabel("Saturation")
    ax.set_zlabel("Value")

    plt.savefig('./research/' + chemical + '/hsv_3d.png')
    plt.show()
    ax.clear()

    # Linear plots 
    plt.scatter(values, hues)
    plt.scatter(values, sat)
    plt.scatter(values, val)
    plt.legend(('Hue','Saturation','Value'))

    plt.title(chemical + '_hsv_linear')
    plt.xlabel(chemical)
    plt.ylabel('value')
    plt.savefig('./research/' + chemical + '/hsv_scale.png')
    plt.show()

    # 3D Plot
    fig = plt.figure()
    ax = Axes3D(fig)

    for key in scale:
        red.append(scale[key][0])
        green.append(scale[key][1])
        blue.append(scale[key][2])

        ax.text(red[-1],green[-1],blue[-1],str(key))

    ax.scatter(red,green,blue)

    ax.set_title(chemical + '_rgb_3d')
    ax.set_xlabel("Red")
    ax.set_ylabel("Green")
    ax.set_zlabel("Blue")

    plt.savefig('./research/' + chemical + '/rgb_3d.png')
    plt.show()
    ax.clear()

    # Linear plots 
    plt.scatter(values, red)
    plt.scatter(values, green)
    plt.scatter(values, blue)
    plt.legend(('Red','Green','Blue'))

    plt.title(chemical + '_rgb_linear')
    plt.xlabel(chemical)
    plt.ylabel('value')
    plt.savefig('./research/' + chemical + '/rgb_linear.png')
    plt.show()


def visualize_interpolation(chemical, actual_rgb, low_rgb, high_rgb):
    palette = np.array([low_rgb[1],
                actual_rgb[1],
                high_rgb[1]])

    indices = np.array([[0,1,2]])

    io.imshow(palette[indices])
    plt.title(chemical + ' ' + str(low_rgb[0]) + ',' + str(actual_rgb[0]) + ',' + str(high_rgb[0]))
    plt.show()

if __name__ == '__main__':

    arg_vals = init.get_args()

    init.init(arg_vals['verbose'])

    create_interpolated_rgb_graph('pH', 5, True)
    create_interpolated_rgb_graph('alkalinity', 5, True)
    create_interpolated_rgb_graph('Cl', 5, True)

    test_values = [['pH',6.8],['pH',7.0],['pH',7.3],['pH',7.4]]

    for value_pair in test_values:
        actual_rgb, low_rgb, high_rgb = interpolate_rgb_values(value_pair[0], value_pair[1])
        visualize_interpolation('pH', actual_rgb, low_rgb, high_rgb)


    create_scale_hue_graph('pH')
#    create_scale_hue_graph('Cl')
#    create_scale_hue_graph('alkalinity')


"""
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
"""