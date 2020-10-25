import RPi.GPIO as GPIO
from time import sleep

class Motor():

    def __init__(self, pins):
        self.frequency = 100
        
        self.Ena, self.In1, self.In2 = pins
        GPIO.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)
        self.pwm = GPIO.PWM(self.Ena, self.frequency)
        self.pwm.start(0)

    def forward(self, speed=50, time=0):
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)
        sleep(time)

    def backward(self, speed=50, time=0):
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)
        sleep(time)

    def stop(self, time=0):
        self.pwm.ChangeDutyCycle(0)
        sleep(time)

    