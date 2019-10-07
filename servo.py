# from gpiozero import Servo
import os
import RPi.GPIO as GPIO
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)

factory = PiGPIOFactory(host='192.168.10.15')
# Seteamos el pin de datos del servoa  un puerto PWM
servo = Servo(18, pin_factory=factory)

while True:
    servo.min()
    sleep(1)
    servo.mid()

    sleep(1)
    servo.max()
    sleep(1)
