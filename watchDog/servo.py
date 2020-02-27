#!venv/bin/python3.6
"""Paquete encargado de la gestión y representación de un dispositivo servo, para reducir la carga a la clase
principal """
from time import sleep

from gpiozero import AngularServo

MIN_PULSE_WIDTH = 35 / 100000  # 0.35ms
MAX_PULSE_WIDTH = 200 / 100000  # 2ms
SPEED = 20 / 1000  # 20ms corresponde con la frecuencia del SG90
SLEEP_TIME = 0.2


class Cerradura(AngularServo):
    """
    Clase que representa el elemento que actuará como cerradura en el sistema
    Cambiamos la especificación por defecto, para poder controlar los 180º que nos permite el modelo de servo SG90
    @see https://gpiozero.readthedocs.io/en/stable/api_output.html#angularservo
    """

    def __init__(self, pin=None, pin_factory=None):
        super(Cerradura, self).__init__(pin, 90, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, SPEED,
                                        pin_factory=pin_factory)
        self.angle = None

    def abrir(self):
        """
        Este método gira el elemento que represente la cerradura hasta una posición que permita mantener la puerta desbloqueda
        """
        self.max()
        sleep(SLEEP_TIME)
        self.angle = None

    def cerrar(self):
        """
        Este método gira el elemento que represente la cerradura hasta una posición que permita mantener la puerta bloqueda
        """
        self.mid()
        sleep(SLEEP_TIME)
        self.angle = None

    def __del__(self):
        if self.is_active:
            self.close()
