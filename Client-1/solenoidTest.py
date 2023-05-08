import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # set GPIO numbering to BCM
GPIO.setup(24, GPIO.OUT)  # set GPIO 18 as output

GPIO.output(24, 0)
  # wait for 1 second
GPIO.output(24, 0)