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

    def __init__(self, port_list, baud_rate, remote_mac=None):
        """Instanciamos una antena XBeee a partir de un dispositivo ZigBeeDevice
        @param port_list Lista de puertos en los que se podría encontrar la antena conectada
        @param baud_rate Frecuencia de trabajo de la antena
        @param remote_mac [Opcional] Dirección mac a de la antena a la que se conectará"""

        """De la lista de posibles puertos a la que pueda estár conectada la antena
        nos conectamos a la primera y lo notificamos"""
        for port in port_list:
            super().__init__(port, baud_rate)
            try:
                super().open()
                if remote_mac is not None:
                    self.remote_Zigbee = remote_mac
            except XBeeException as e:
                print("ERROR: No se ha podido conectar con la antena XBee.\t\n" + str(e))
                super().close()
            else:
                print("Conectada la antena del puerto " + port)
                break

    @property
    def remote_Zigbee(self) -> RemoteZigBeeDevice:
        """
        @return Retorna el dispositivo remoto al que se encuentra conectado la antena
        @rtype: RemoteZigBeeDevice
        """
        return self.__remote

    @remote_Zigbee.setter
    def remote_Zigbee(self, mac):
        self.__remote = RemoteZigBeeDevice(self, mac)
