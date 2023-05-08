import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# fingerprint
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

while True:
    GPIO.output(16,True)
    time.sleep(0.5)
    GPIO.output(16,False)
    time.sleep(0.5)