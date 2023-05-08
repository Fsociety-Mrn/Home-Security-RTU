import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# fingerprint
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

# Ultrasonic Sensor

# buzzer
GPIO.setup(16, GPIO.OUT)

# Buton
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_UP)


def buzzer():
    GPIO.output(16,True)
    time.sleep(0.5)
    GPIO.output(16,False)
    time.sleep(0.5)

while True:
    print(GPIO.input(26))
    if GPIO.input(26):
        buzzer()
    else:
      GPIO.output(16,False)
