from gpiozero import Servo, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Declaración de los pines que vamos a usar
servo_pin = 17
ok_led_pin = 25
warn_led_pin = 26
error_led_pin = 6
monitor_led_pin = 16

# factory = PiGPIOFactory(host='192.168.10.15')
# Seteamos el pin de datos del servo  un puerto PWM
servo = Servo(servo_pin)
# Seteo de los pines
ok_led = LED(ok_led_pin)
warn_led = LED(warn_led_pin)
error_led = LED(error_led_pin)
monitor_led = LED(monitor_led_pin)

print("Empezamos")

for x in range(5):
    ok_led.blink(1, 1, 5)
    warn_led.blink(1, 1, 5)
    error_led.blink(1, 1, 5)
    monitor_led.blink(1, 1, 5)
    print(servo)
    servo.min()
    print(servo)
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)
    print(x)

print("e voila")
