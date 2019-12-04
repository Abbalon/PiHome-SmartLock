"""Paquete que controla los ficheros de configuración del proyecto"""

# Cargamos los datos del fichero de configuración
import os
from configparser import ConfigParser
from os import scandir, getcwd
from os.path import abspath


def read_config(cfg_files):
    """
Lee los parámetros fijados en los ficheros de configuración
    :param cfg_files:
    :return:
    """
    if cfg_files is not None:
        config_properties = ConfigParser()

        # merges all files into a single config
        for i, cfg_file in enumerate(cfg_files):
            if os.path.exists(cfg_file):
                config_properties.read(cfg_file)

        return config_properties


def ls_file(ruta=getcwd()):
    """

    :param ruta:
    :return:
    """
    return [arch.name for arch in scandir(ruta)]


def ls_a(ruta=getcwd()):
    """

    :param ruta:
    :return:
    """
    return [abspath(arch.path) for arch in scandir(ruta)]


ls_file()

# merge all into one config dictionary
parameters = read_config(['env.ini', 'local.ini'])

__project = None
__version = None
__description = None
__autor = None

"""Definición de las variables de configuración"""
# Dirección del host remoto
remote_host = None

# LED's
pin_error = None
pin_warn = None
pin_monitor = None
pin_success = None
# Servo
pin_servo = None
# XBee
xbee_baudrate = None
xbee_route = None
mac_puerta = None
mac_router = None

# Variable para definir si la ejecución es en remoto o en local
remote = False

# Recuperamos la información del fichero de configuración
if parameters.__len__() > 1:
    # get the current branch (from local.ini)
    env = parameters.get('branch', 'env')
    remote = parameters.get('branch', 'remote')
    remote_host = parameters.get('remote', 'host')  # Configurado en local.ini

    # proceed to point everything at the 'branched' resources
    dbUrl = parameters.get(env + '.mysql', 'dbUrl')
    dbUser = parameters.get(env + '.mysql', 'dbUser')
    dbPwd = parameters.get(env + '.mysql', 'dbPwd')
    dbName = parameters.get(env + '.mysql', 'dbName')

    # global values
    __project = parameters.get('global', '__project__')
    __version = parameters.get('global', '__version__')
    __description = parameters.get('global', '__description__')
    __autor = parameters.get('global', '__autor__')

    # Carga de los pines
    pin_error = parameters.get('pin', 'error')
    pin_warn = parameters.get('pin', 'warn')
    pin_monitor = parameters.get('pin', 'monitor')
    pin_success = parameters.get('pin', 'success')
    pin_servo = parameters.get('pin', 'servo')

    # Info del xbee
    xbee_baudrate = parameters.get('xbee', 'baudrate')
    xbee_route = parameters.get('xbee', 'route')
    mac_puerta = parameters.get('xbee.mac', 'puerta')
    mac_router = parameters.get('xbee.mac', 'router')
