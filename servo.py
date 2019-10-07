from gpiozero import Servo
from time import sleep

# Seteamos el pin de datos del servoa  un puerto PWM
servo = Servo(18)

while True:
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)