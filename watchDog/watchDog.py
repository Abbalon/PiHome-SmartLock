#!venv/bin/python
"""Código para la gestionar el acceso a un recinto.
El sistema leera una tarjeta MFRC522, la cotejará con el sistema central, mandando la id de la tarjeta mediante Zigbee
Si la respuesta es afirmativa, abrirá la cerradura de la puerta representada con un serbo, y pintará el LED verde, en
caso contrário, pintará el led rojo"""
from time import sleep
from typing import List

from digi.xbee.exception import XBeeException
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory

import config
from .MFRC522 import MFRC522
from .servo import Cerradura
from .xbee import XBee

APAGAR = "SLEEP"
CMD = "CMD"


class WatchDog:
    """Representa el dispositivo que regulará el control de acceso"""

    @property
    def ok_led(self):
        """

        @return:
        """
        return self._ok_led

    @property
    def warn_led(self):
        """

        @return:
        """
        return self._warn_led

    @property
    def error_led(self):
        """

        @return:
        """
        return self._error_led

    @property
    def monitor_led(self):
        """

        @return:
        """
        return self._monitor_led

    @property
    def cerradura(self):
        """

        @return:
        """
        return self._cerradura

    @property
    def antena(self):
        """

        @return:
        """
        return self._antena

    @property
    def reader_tag(self):
        """

        @return:
        """
        return self._reader

    def __init__(self, remote):
        print("Inicializando WatchDog\n\tModo Local:\t" + str((remote == 'False')))
        try:
            if remote and remote == 'True':
                assert config.remote_host, "No se ha encontrado la dirección remota donde ejecutarse"
                print("Cargando configuración para ejecución en remoto.\n")
                factory = PiGPIOFactory(host=config.remote_host)
                # Seteamos el pin de datos del servo  un puerto PWM
                self.cerradura = Cerradura(config.pin_servo, pin_factory=factory)
                # Seteo de los pines
                self.ok_led = LED(config.pin_success, pin_factory=factory)
                self.warn_led = LED(config.pin_warn, pin_factory=factory)
                self.error_led = LED(config.pin_error, pin_factory=factory)
                self.monitor_led = LED(config.pin_monitor, pin_factory=factory)
            else:
                print("Cargando configuración para ejecución en local.\n")
                # Seteamos el pin de datos del servo  un puerto PWM
                self.cerradura = Cerradura(config.pin_servo)
                # Seteo de los pines
                self.ok_led = LED(config.pin_success)
                self.warn_led = LED(config.pin_warn)
                self.error_led = LED(config.pin_error)
                self.monitor_led = LED(config.pin_monitor)

            # Configuramos la antena Xbee
            self.antena = XBee(config.xbee_port, config.xbee_baudrate, config.mac_puerta)
            self.__im_active = True

            # Configuramos el lector de MFRC522
            self.reader_tag = MFRC522()

            print("Inicialización de WacthDog correcta\n")

        except Exception as e:
            print(str(e))
            raise

    def wake_up(self):
        """
        Hablilitamos la funcionalidad de la puerta
        :return:
        """
        print("Stapleton se ha despertado.")

        msg_pool = []
        while self.__im_active:
            self.merodear(msg_pool)

        for x in range(5):
            self.cerradura.abrir()
            self.ok_led.blink(1, 1, 5)
            self.warn_led.blink(1, 1, 5)
            self.error_led.blink(1, 1, 5)
            self.monitor_led.blink(1, 1, 5)
            sleep(5)
            self.cerradura.cerrar()
            print(x)

        print("et voila")

    def merodear(self, msg_pool: list):
        """Tratamos la información que recibamos
           @param msg_pool:
        """
        max_try_reconnect: int = 5
        try:
            if self.antena.is_open:
                recived_order = self.antena.read_data()

                if recived_order is not None:
                    msg = str(recived_order.data.decode("utf8"))
                    if msg.startswith(CMD):
                        self.ejecutar_accion_progamada(msg.split(':'))
                    else:
                        self.monitor_led.blink(0.2, 0.2, 3)
                        print(msg)

            self.olfatear()

        except XBeeException as e:
            print("WARN: Parece que se ha desconectado la antena o hay más procesos accediendo a ella\n\t" + str(e))
            for x in range(max_try_reconnect):
                self.antena = XBee(config.xbee_port, config.xbee_baudrate, config.mac_puerta)
                if self.antena.is_open:
                    break

    def olfatear(self) -> None:
        """
            Método mediante el cual se reconocerá el tag presentado
            @rtype: None
        """
        self.reader_tag.oler()

    def __sleep(self):
        self.__im_active = False
        self.apagar_leds()
        print("VAMOS!!!!")

    def __del__(self):
        """Cerramos los elementos que podrían ser peligrosos que se quedasen prendidos"""
        # Dejamos 5 seg, antes de cerrar tod0, para cerrar las conexiones correctamente
        sleep(5)

        try:
            if self.cerradura and not self.cerradura.closed:
                self.cerradura.close()
        except AttributeError:
            print("Parece que no se había creado la cerradura")

        try:
            if self.antena and self.antena.is_open():
                self.antena.close()
        except AttributeError:
            print("Parece que no se había creado la antena")

        self.apagar_leds()
        print("Stapleton se ha vuelto a dormir")

    @cerradura.setter
    def cerradura(self, value):
        self._cerradura = value

    @ok_led.setter
    def ok_led(self, value):
        self._ok_led = value

    @warn_led.setter
    def warn_led(self, value):
        self._warn_led = value

    @error_led.setter
    def error_led(self, value):
        self._error_led = value

    @monitor_led.setter
    def monitor_led(self, value):
        self._monitor_led = value

    @antena.setter
    def antena(self, value):
        self._antena = value

    @reader_tag.setter
    def reader_tag(self, value):
        self._reader = value

    def ejecutar_accion_progamada(self, order_list: List[str]):
        """
            Con este método se encapsulan todas las acciones previstas para las ordenes recibidas
        """
        # Comprobamos que el primer parámetro sea un comando
        order: str = str(order_list.pop())
        if order == APAGAR:
            self.warn_led.blink()
            self.__sleep()
        if order == "ABRIR":
            self.ok_led.blink(0.2, 0.2, 2)
            self.cerradura.abrir()
        if order == "CERRAR":
            self.ok_led.blink(0.2, 0.2, 2)
            self.cerradura.cerrar()
        if order == "ECHO":
            status = "Cerradura[" + str(self.cerradura.is_active) + ", " + str(self.cerradura.value) + "]\n"
            status += "Antena[" + str(self.antena) + "]\n"
            self.antena.mandar_mensage(status)

    def apagar_leds(self):
        """
            Apaga los leds de monitorizace, warning, error y ok
        """
        self.monitor_led.off()
        self.ok_led.off()
        self.warn_led.off()
        self.error_led.off()
