#!venv/bin/python3.6
"""Clase que carga la configuración del proyecto"""

# a simple function to read an array of configuration files into a config object

from setuptools import setup, find_packages

import config

setup(
    name=config.__project,
    version=config.__version,
    description=config.__description,
    author=config.__autor,
    # url='hhtp://joebloggsblog.com',
    packages=find_packages(),  # ['watchDog'],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    # scripts=['path/to/your/script'],
)
