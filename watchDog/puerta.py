#!venv/bin/python3.6
"""Código para la gestionar el acceso a un recinto.
El sistema leera una tarjeta RFID, la cotejará con el sistema central, mandando la id de la tarjeta mediante Zigbee
Si la respuesta es afirmativa, abrirá la cerradura de la puerta representada con un serbo, y pintará el LED verde, en
caso contrário, pintará el led rojo"""
from time import sleep

from digi.xbee.devices import ZigBeeDevice, RemoteZigBeeDevice
from gpiozero import Servo, LED
from gpiozero.pins.pigpio import PiGPIOFactory

import config

# Definición de variables
sg90 = None
ok_led = None
warn_led = None
error_led = None
monitor_led = None

# Configuración condicional atendiendo a si el código se ejecuta en local
# o desde otra máquina
if config.remote:
    factory = PiGPIOFactory(host=config.remote_host)
    # Seteamos el pin de datos del servo  un puerto PWM
    servo = Servo(config.pin_servo, pin_factory=factory)
    # Seteo de los pines
    ok_led = LED(config.pin_success, pin_factory=factory)
    warn_led = LED(config.pin_warn, pin_factory=factory)
    error_led = LED(config.pin_error, pin_factory=factory)
    monitor_led = LED(config.pin_monitor, pin_factory=factory)
else:
    # Seteamos el pin de datos del servo  un puerto PWM
    servo = Servo(config.pin_servo)
    # Seteo de los pines
    ok_led = LED(config.pin_success)
    warn_led = LED(config.pin_warn)
    error_led = LED(config.pin_error)
    monitor_led = LED(config.pin_monitor)

# Configuramos la antena Xbee
xbee = ZigBeeDevice(config.xbee_route, config.xbee_baudrate)
remote_xbee = RemoteZigBeeDevice(xbee, config.mac_puerta)

print("Empezamos")

for x in range(5):
    ok_led.blink(1, 1, 5)
    warn_led.blink(1, 1, 5)
    error_led.blink(1, 1, 5)
    monitor_led.blink(1, 1, 5)
    print(servo.value)
    servo.min()
    print(servo.value)
    sleep(5)
    servo.mid()
    sleep(5)
    servo.max()
    sleep(5)
    print(x)

print("e voila")
