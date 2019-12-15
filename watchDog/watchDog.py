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


class WatchDog:
    """Representa el dispositivo que regulará el control de acceso"""

    def __init__(self, remote=config.remote):

        if remote:
            factory = PiGPIOFactory(host=config.remote_host)
            # Seteamos el pin de datos del servo  un puerto PWM
            self.servo = Servo(config.pin_servo, pin_factory=factory)
            # Seteo de los pines
            self.ok_led = LED(config.pin_success, pin_factory=factory)
            self.warn_led = LED(config.pin_warn, pin_factory=factory)
            self.error_led = LED(config.pin_error, pin_factory=factory)
            self.monitor_led = LED(config.pin_monitor, pin_factory=factory)
        else:
            # Seteamos el pin de datos del servo  un puerto PWM
            print(config.pin_servo)
            self.servo = Servo(config.pin_servo)
            # Seteo de los pines
            self.ok_led = LED(config.pin_success)
            self.warn_led = LED(config.pin_warn)
            self.error_led = LED(config.pin_error)
            self.monitor_led = LED(config.pin_monitor)

        # Configuramos la antena Xbee
        self.xbee = ZigBeeDevice(config.xbee_route, config.xbee_baudrate)
        self.remote_xbee = RemoteZigBeeDevice(self.xbee, config.mac_puerta)

    def wake_up(self):
        """
        Hablilitamos la funcionalidad de la puerta
        :return:
        """
        print("Empezamos")

        for x in range(5):
            self.ok_led.blink(1, 1, 5)
            self.warn_led.blink(1, 1, 5)
            self.error_led.blink(1, 1, 5)
            self.monitor_led.blink(1, 1, 5)
            print(self.servo.value)
            self.servo.min()
            print(self.servo.value)
            sleep(5)
            self.servo.mid()
            sleep(5)
            self.servo.max()
            sleep(5)
            print(x)

        print("et voila")

    def __del__(self):
        """Cerramos los elementos que podría ser peligrosos que se quedasen prendidos"""
        self.servo.close()
        self.xbee.close()
        print("c'est fini de la mate")
