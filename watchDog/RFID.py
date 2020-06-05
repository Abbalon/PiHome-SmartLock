#!venv/bin/python
"""
    Paquete encargado de la gestión y representación de un dispositivo lector de tarjetas RFID.
    Como el sistema sobre el que se está desarrollando es una Raspberry Pi Zero, tras activar el controlador del puerto SPI,
    tenemos que los dos puertos disponibles son: /dev/spidev0.0 (para el ejemplo usaremos el 0 - pin(24) - GPIO8 - SPICS0 ) y /dev/spidev0.1

"""
from mfrc522 import SimpleMFRC522


class RFID(object):
    """
    Clase que representa el dispositivo lector de tarjetas RFID
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
        self.device = SimpleMFRC522()

    def leer_tarjeta(self) -> str:
        """
            Lee la tarjeta sin bloquear el proceso y retona la id de la misma
        """
        try:
            # id, text = self.device.read()
            id = self.device.read_id_no_block()
            return str(id)
        except Exception as ki:
            print("Error: " + str(ki))
            raise

    def esperar_hasta_leer_tarjeta(self) -> str:
        """
            Lee la tarjeta sin bloquear el proceso y retona la id de la misma
        """
        try:
            id = self.device.read_id()
            return id
        except Exception as ki:
            print("Error: " + str(ki))
            raise
