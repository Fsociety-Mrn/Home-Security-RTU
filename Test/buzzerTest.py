import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# fingerprint
GPIO.setup(6, GPIO.OUT, initial=GPIO.HIGH)


 