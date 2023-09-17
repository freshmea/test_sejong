import RPi.GPIO as g 
import time 

servo_pin = 12

g.setmode(g.BCM)

g.setup(servo_pin, g.OUT)

pwm = g.PWM(servo_pin, 50)
pwm.start(3.0)
time.sleep(0.5)

for i in range(5):
    pwm.ChangeDutyCycle(3.0)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(9.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(12.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(9.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    
pwm.stop()
g.cleanup()

