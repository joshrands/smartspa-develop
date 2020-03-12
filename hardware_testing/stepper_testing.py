import RPi.GPIO as GPIO
import time

step_pin = 40
dir_pin = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
#GPIO.output(dir_pin, True)

try:
#    while True:
    print("On")
    for i in range(0,200):
        GPIO.output(step_pin, True)
        time.sleep(.005)
        GPIO.output(step_pin, False)
        time.sleep(.005)

    print("Off")
    time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

