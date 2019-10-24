# a simple function to read an array of configuration files into a config object
import os
from configparser import ConfigParser

from setuptools import setup, find_packages


def read_config(cfg_files):
    if cfg_files is not None:
        config_properties = ConfigParser()

        # merges all files into a single config
        for i, cfg_file in enumerate(cfg_files):
            if os.path.exists(cfg_file):
                config_properties.read(cfg_file)

        return config_properties


# merge all into one config dictionary
config = read_config(['env.ini', 'local.ini'])

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

# Variable para definir si la ejecución es en remoto o en local
remote = False

# Recuperamos la información del fichero de configuración
if config is not None:
    # get the current branch (from local.ini)
    env = config.get('branch', 'env')
    remote = config.get('branch', 'remote')
    remote_host = config.get('remote', 'host')  # Configurado en local.ini

    # proceed to point everything at the 'branched' resources
    dbUrl = config.get(env + '.mysql', 'dbUrl')
    dbUser = config.get(env + '.mysql', 'dbUser')
    dbPwd = config.get(env + '.mysql', 'dbPwd')
    dbName = config.get(env + '.mysql', 'dbName')

    # global values
    __project = config.get('global', '__project__')
    __version = config.get('global', '__version__')
    __description = config.get('global', '__description__')
    __autor = config.get('global', '__autor__')

    # Carga de los pines
    pin_error = config.get('pin', 'error')
    pin_warn = config.get('pin', 'warn')
    pin_monitor = config.get('pin', 'monitor')
    pin_success = config.get('pin', 'success')
    pin_servo = config.get('pin', 'monitor')

    # Info del xbee
    xbee_baudrate = config.get('xbee', 'baudrate')
    xbee_route = config.get('xbee', 'route')

setup(
    name=__project,
    version=__version,
    description=__description,
    author=__autor,
    # url='hhtp://joebloggsblog.com',
    packages=find_packages(),  # ['watchDog'],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    # scripts=['path/to/your/script'],
)
