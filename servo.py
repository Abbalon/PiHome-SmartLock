from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory('192.168.10.15')
# Seteamos el pin de datos del servo  un puerto PWM
servo = Servo(17, pin_factory=factory)

print("Empezamos")
for x in range(5):
    print(x)
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)
    print(servo.value)

print("Sha'cabo")
