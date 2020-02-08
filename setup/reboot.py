import subprocess
import time

command = "/usr/bin/sudo /sbin/reboot"

print("Power cycling SmartSpa system...")
time.sleep(10)

process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]
print(output)

