#!venv/bin/python3.6
"""Paquete encargado de la gestión y representación de un dispositivo ZigBee/Xbee"""

import serial.tools.list_ports
from digi.xbee.devices import ZigBeeDevice, RemoteZigBeeDevice
from digi.xbee.exception import XBeeException

"""Lista de palabras que podría contener un shield con una antena xbee"""
xbeeAntenaWhiteList = ['FT232R', 'USB', 'UART']


def encontrar_rutas() -> []:
    """Método que retorna una lista de posibles rutas donde se encontrará un dispositivo compatible con una antena
     XBEE conectada mediante un shield USB"""

    ports = serial.tools.list_ports.comports()
    filtered = []
    for port, desc, hwid in sorted(ports):
        for word in desc.split(' '):
            if word in xbeeAntenaWhiteList:
                filtered.append(port)
                break
    return filtered


class XBee(ZigBeeDevice):
    """Clase que representa las antenas xbee que serán la principàl interface de comunicación del dispositivo
    WatchDog"""

    def __init__(self, port_list, baud_rate):
        """Instanciamos una antena XBeee a partir de un dispositivo ZigBeeDevice"""

        """De la lista de posibles puertos a la que pueda estár conectada la antena
        nos conectamos a la primera y lo notificamos"""
        for port in port_list:
            super().__init__(port, baud_rate)
            try:
                print(super()._get_operating_mode())
                super().open()
            except XBeeException as e:
                print("ERROR: No se ha podido conectar con la antena XBee.\t\n" + str(e))
                super().close()
            else:
                print("Conectada la antena del puerto " + port)
                break

    def get_remote_Zigbee(self, mac) -> RemoteZigBeeDevice:
        """
        Retorna un zigBee remoto asociado a esta antena
        @param mac: dirección mac del destino
        @return:
        """
        return RemoteZigBeeDevice(self, mac)
