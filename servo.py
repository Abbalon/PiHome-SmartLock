from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory('192.168.10.15')
# Seteamos el pin de datos del servoa  un puerto PWM
servo = Servo(18, pin_factory=factory)

while True:
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)
