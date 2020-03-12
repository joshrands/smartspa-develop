import RPi.GPIO as GPIO
import time

servo_pin = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)

p = GPIO.PWM(servo_pin, 50)
p.start(2.5)

try:
    while True:
        p.ChangeDutyCycle(2.5)
        print("Duty cycle at 0")
        time.sleep(5)
        p.ChangeDutyCycle(7.5)
        print("Duty cycle at 7.5")
        time.sleep(5)
        p.ChangeDutyCycle(15)
        time.sleep(5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()

