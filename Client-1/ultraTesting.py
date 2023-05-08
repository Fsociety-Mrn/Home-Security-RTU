import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# fingerprint
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)

# Ultrasonic Sensor

# TRIGGER
GPIO.setup(21, GPIO.OUT)

# ECHO
GPIO.setup(20, GPIO.IN)


while True:
    
    GPIO.output(21,False)
    time.sleep(0.5)
    GPIO.output(21,True)
    time.sleep(0.00001)
    GPIO.output(21,False)
    
    pulse_start,pulse_end = 0,0
    while GPIO.input(20) == 0:
        pulse_start = time.time()
        
    while GPIO.input(20) == 1:
        pulse_end = time.time()
        
    distance = (pulse_end-pulse_start) * 17150
    inches = round(distance / 2.54, 1)
    print(inches)    