#!venv/bin/python
"""
    Paquete encargado de la gestión y representación de un dispositivo lector de tarjetas MFRC522.
    Como el sistema sobre el que se está desarrollando es una Raspberry Pi Zero, tras activar el controlador del puerto SPI,
    tenemos que los dos puertos disponibles son: /dev/spidev0.0 (para el ejemplo usaremos el 0 - pin(24) - GPIO8 - SPICS0 ) y /dev/spidev0.1

"""

# import mfrc522
from mfrc522 import SimpleMFRC522


class MFRC522(object):
    """
    Clase que representa el dispositivo lector de tarjetas MFRC522
    """

    CHANNEL: int = 0
    CHIP_SELECT: int = 0

    @property
    def device(self):
        """
        Dispositivo que encaspulará el objeto de la librería externa que se represente
        @return:
        """
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    def __init__(self):
        self._device = SimpleMFRC522()

    def oler(self):
        """
            Lee la targeta
        """
        try:
            # id, text = self.device.read()
            id = self.device.read_id_no_block()
            if id is not None:
                print("ID: %s\n" % id)
        except Exception as ki:
            print("Error: " + str(ki))
            raise
