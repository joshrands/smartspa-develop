from helpers import *
import argparse

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

parser = argparse.ArgumentParser()
parser.add_argument("--vis", action='store_true', help="Visualize input")
parser.add_argument("--rgb", action='store_true', help="Show rgb visualization")
parser.add_argument("--std")
parser.add_argument("--file")
parser.add_argument("--scale")

args = parser.parse_args()
arg_vals = vars(args)

vis = arg_vals['vis']
rgb_vis = arg_vals['rgb']
std = arg_vals['std']
file_name = arg_vals['file']
scale = arg_vals['scale']

if (file_name == None):
	file_name = input("Enter file name: ")
if (std == None):
	std = 2

file_name = "test/" + file_name

r,g,b = getRGBOfImage(file_name, rgb_vis, int(std))
#print(r,g,b)

if (scale == None):
	scale = "pH"

scale = getScaleMap(scale)
#print(scale)

s_r = []
s_g = []
s_b = []

fig = pyplot.figure()
ax = Axes3D(fig)

for key in scale:
	print(key)
	rgb = scale[key]
	s_r.append((rgb[0]))
	s_g.append((rgb[1]))
	s_b.append((rgb[2]))

	ax.text(s_r[-1],s_g[-1],s_b[-1],str(key))

if vis:
	ax.scatter(r,g,b)
	ax.text(r,g,b,"Raw Unknown")

	ax.scatter(s_r,s_g,s_b)

	ax.set_xlabel("Red")
	ax.set_ylabel("Green")
	ax.set_zlabel("Blue")

# check r,g,b ranges
if r > max(s_r):
	r = max(s_r)
if r < min(s_r):
	r = min(s_r)

if g > max(s_g):
	g = max(s_g)
if g < min(s_g):
	g = min(s_g)

if b > max(s_b):
	b = max(s_b)
if b < min(s_b):
	b = min(s_b)

if vis:
	ax.scatter(r,g,b)
	ax.text(r,g,b,"Cleaned Unknown")

	pyplot.show()
	pyplot.close()

# get distance from each point 
closest = 255
closest_key = ""
for key in scale:
	rgb = scale[key]

	dist = getDistanceBetweenPoints(rgb, [r,g,b])
	print(key + ": " + str(dist))

	if (dist < closest):
		closest = dist
		closest_key = key	

print("Closest to: " + closest_key)

