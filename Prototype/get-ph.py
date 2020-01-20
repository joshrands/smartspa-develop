from helpers import *
import argparse

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

parser = argparse.ArgumentParser()
parser.add_argument("--vis", action='store_true', help="Visualize input")
args = parser.parse_args()
arg_vals = vars(args)

vis = arg_vals['vis']

file_name = input("Enter file name: ")
r,g,b = getRGBOfImage(file_name)
#print(r,g,b)

scale = getScaleMap("pH")
#print(scale)

if vis:
	fig = pyplot.figure()
	ax = Axes3D(fig)
	ax.scatter(r,g,b)
	ax.text(r,g,b,"Unknown")

	r = []
	g = []
	b = []
	for key in scale:
		print(key)
		rgb = scale[key]
		r.append((rgb[0]))
		g.append((rgb[1]))
		b.append((rgb[2]))
		
		ax.text(r[-1],g[-1],b[-1],str(key))

	ax.scatter(r,g,b)

#	ax.set_xlim(0,255)
#	ax.set_ylim(0,255)
#	ax.set_zlim(0,255)
	ax.set_xlabel("Red")
	ax.set_ylabel("Green")
	ax.set_zlabel("Blue")
	
	pyplot.show()

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

