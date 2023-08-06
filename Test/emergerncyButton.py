import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



# Ultrasonic Sensor

# buzzer
GPIO.setup(6, GPIO.OUT)

# Buton
GPIO.setup(5, GPIO.IN,pull_up_down=GPIO.PUD_UP)


def buzzer():
    GPIO.output(6,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(6,GPIO.LOW)
    time.sleep(0.5)

while True:

    # kpaag nag 1 ibig sabihin nagana to
    print(GPIO.input(5))
#while True:
#    print(GPIO.input(25))
    if GPIO.input(5):
       buzzer()
    else:
     GPIO.output(6,False)
