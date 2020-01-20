from helpers import *
import argparse

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

parser = argparse.ArgumentParser()
parser.add_argument("--vis", action='store_true', help="Visualize input")
args = parser.parse_args()
arg_vals = vars(args)

vis = arg_vals['vis']

file_name = "test-ph.png"#input("Enter file name: ")
r,g,b = getRGBOfImage(file_name)
#print(r,g,b)

scale = getScaleMap("pH")
#print(scale)

fig = pyplot.figure()
ax = Axes3D(fig)
ax.scatter(r,g,b)
ax.text(r,g,b,"Unknown")

r_arr = []
g_arr = []
b_arr = []
for key in scale:
	rgb = scale[key]
	r_arr.append((rgb[0]))
	g_arr.append((rgb[1]))
	b_arr.append((rgb[2]))
	
	ax.text(r_arr[-1],g_arr[-1],b_arr[-1],str(key))

ax.scatter(r_arr,g_arr,b_arr)

#	ax.set_xlim(0,255)
#	ax.set_ylim(0,255)
#	ax.set_zlim(0,255)
ax.set_xlabel("Red")
ax.set_ylabel("Green")
ax.set_zlabel("Blue")

if vis:	
	pyplot.show()

r_range = max(r_arr) - min(r_arr)
g_range = max(g_arr) - min(g_arr)
b_range = max(b_arr) - min(b_arr)

# normalize input data
r = (r - min(r_arr)) / r_range
g = (g - min(g_arr)) / g_range
b = (b - min(b_arr)) / b_range

# get distance from each point 
closest = 255
closest_key = ""
for key in scale:
	rgb = scale[key]

	rgb[0] = (rgb[0] - min(r_arr)) / r_range
	rgb[1] = (rgb[1] - min(g_arr)) / g_range
	rgb[2] = (rgb[2] - min(b_arr)) / b_range

	dist = getDistanceBetweenPoints(rgb, [r,g,b])
	print(key + ": " + str(dist))

	if (dist < closest):
		closest = dist
		closest_key = key	

print("Closest to: " + closest_key)

