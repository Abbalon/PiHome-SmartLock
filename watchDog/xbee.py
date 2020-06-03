#!env/bin/python3.8
"""Paquete encargado de la gestión y representación de un dispositivo ZigBee/Xbee"""

import serial.tools.list_ports
from digi.xbee.devices import ZigBeeDevice, RemoteZigBeeDevice
from digi.xbee.exception import XBeeException
from digi.xbee.models.address import XBee64BitAddress, XBee16BitAddress
from digi.xbee.models.message import XBeeMessage

"""Lista de palabras que podría contener un shield con una antena xbee"""
xbeeAntenaWhiteList = ['FT232R', 'UART']


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
    WatchDog
    @see https://xbplib.readthedocs.io/en/stable/index.html"""

    def __init__(self, port_list, baud_rate, remote_mac=None):
        """Instanciamos una antena XBeee a partir de un dispositivo ZigBeeDevice
        @param port_list Lista de puertos en los que se podría encontrar la antena conectada
        @param baud_rate Frecuencia de trabajo de la antena
        @param remote_mac [Opcional] Dirección mac a de la antena a la que se conectará"""

        print("Creando la antena")
        """De la lista de posibles puertos a la que pueda estár conectada la antena
        nos conectamos a la primera y lo notificamos"""
        print("Puertos encontrados: " + str(port_list))
        print("Frecuencia de trabajo: " + str(baud_rate))
        print("Enlace remoto: " + str(remote_mac))
        for port in port_list:
            print("Probando el puerto: " + port)
            try:
                super().__init__(port, baud_rate)
            except Exception as e:
                print("Encontrado un error al inicializar el dispositivo ZigBeeDevice")
                print(str(e))
                raise e

            try:
                super().open()
                if remote_mac is not None:
                    self.remote_Zigbee = remote_mac

                # Nos disponemos a escuchar el medio
                # super().add_data_received_callback(self.__tratar_entrada)
            except XBeeException as e:
                print("ERROR: No se ha podido conectar con la antena XBee.\n\t" + str(e))
                super().close()
            else:
                antena = str(super().get_node_id() + "(" + str(super().get_64bit_addr()) + ")")
                print("\tConectada la antena '" + antena + "' al puerto " + port + "\n")
                break

    def __del__(self):
        print("Voy a dejar de escuchar")
        try:
            super().del_data_received_callback(self.__tratar_entrada)
        except Exception as e:
            print("ERROR: No se ha cerrado la conexíón de la antena\n\t" + str(e))

    @property
    def remote_Zigbee(self) -> RemoteZigBeeDevice:
        """
        @return Retorna el dispositivo remoto al que se encuentra conectado la antena
        @rtype: RemoteZigBeeDevice
        """
        return self.__remote

    @remote_Zigbee.setter
    def remote_Zigbee(self, mac):
        self.__remote = RemoteZigBeeDevice(self, XBee64BitAddress.from_hex_string(mac))

    def mandar_mensage(self, msg="Hello"):
        """
            Manda el mensaje al destinatario por defecto
        """
        # Transformamos el mensaje recibido en un string tratable
        msg = str(msg)
        # Recuperamos la dirección del dispositivo remoto en formato de 64 bits
        high = self.remote_Zigbee.get_64bit_addr()
        # Recuperamos la dirección del dispositivo remoto en 16 bits o la marcamos como desconocida
        low = self.remote_Zigbee.get_16bit_addr() or XBee16BitAddress.UNKNOWN_ADDRESS
        try:
            # Intentamos mandar el mensaje
            super().send_data_64_16(high, low, msg)
            # super().send_expl_data(self.remote_Zigbee, msg)
        except Exception as e:
            print("Se ha encontrado un error al mandar el mensaje\n\t" + str(e))
            # Añadir código para el reintento
        else:
            # TODO Borrar esta traza de control
            print("Mandado mensaje:\t" + msg)

    def __tratar_entrada(self, recived_msg: XBeeMessage):
        """
            Tratamos la información que recibamos
        @param recived_msg:
        """
        msg = recived_msg.data.decode("utf8")
        print(msg)
        super().close()
