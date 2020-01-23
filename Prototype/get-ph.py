from helpers import *
import argparse

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

parser = argparse.ArgumentParser()
parser.add_argument("--vis", action='store_true', help="Visualize input")
parser.add_argument("--rgb", action='store_true', help="Show rgb visualization")
parser.add_argument("--std")

args = parser.parse_args()
arg_vals = vars(args)

vis = arg_vals['vis']
rgb_vis = arg_vals['rgb']
std = arg_vals['std']

file_name = input("Enter file name: ")
r,g,b = getRGBOfImage(file_name, rgb_vis, int(std))
#print(r,g,b)

scale = getScaleMap("pH")
#print(scale)

if vis:
	fig = pyplot.figure()
	ax = Axes3D(fig)
	ax.scatter(r,g,b)
	ax.text(r,g,b,"Unknown")

	s_r = []
	s_g = []
	s_b = []
	for key in scale:
		print(key)
		rgb = scale[key]
		s_r.append((rgb[0]))
		s_g.append((rgb[1]))
		s_b.append((rgb[2]))
		
		ax.text(s_r[-1],s_g[-1],s_b[-1],str(key))

	ax.scatter(s_r,s_g,s_b)

#	ax.set_xlim(0,255)
#	ax.set_ylim(0,255)
#	ax.set_zlim(0,255)
	ax.set_xlabel("Red")
	ax.set_ylabel("Green")
	ax.set_zlabel("Blue")
	
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

