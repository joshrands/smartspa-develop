#!/home/josh/anaconda3/bin/python

import sys
import subprocess

network = sys.argv[1]
password = sys.argv[2]

print("[PYTHON]: Connecting to network: '%s' with password: '%s'" % (network, password))

# write to wpa_supplicant file
wpa_supp = open("/etc/wpa_supplicant/wpa_supplicant.conf","a") # open in append mode!!!

wpa_supp.write("network={\n")
wpa_supp.write("\tssid=\"" + network + "\"\n")
wpa_supp.write("\tpsk=\"" + password + "\"\n")
wpa_supp.write("}\n\n")

# TODO: do other initial system setup stuff...


