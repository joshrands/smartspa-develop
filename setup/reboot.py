import subprocess

command = "/usr/bin/sudo /sbin/reboot"

process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]
print(output)

