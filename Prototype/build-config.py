# build config files from input images 

from helpers import *
import os

scale_name = input("Enter scale name: ")

def buildConfig(scale_name):
	directory = os.fsencode("config/" + scale_name)
	out_file = open(scale_name + "-config.csv","w")
#	out_file.write(scale_name + "\n")

	for file in os.listdir(directory):
		file_name = os.fsdecode(file)
		file_path = "config/" + scale_name + "/" + file_name	
		r,g,b = getRGBOfImage(file_path)

		print(r,g,b)

		# write to config file
		# get pH 
		nums = file_name.split(',')
		whole = nums[0]
		decimal = nums[1].split('.')[0]

		out_file.write(whole + "." + decimal + ",")
		out_file.write("(" + str(r) + " " + str(g) + " " + str(b) + ")\n")
	
	out_file.close()

# pH
buildConfig(scale_name)

