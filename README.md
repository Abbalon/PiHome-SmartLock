# Zero-Project
___
***Zero-Project***, es el módulo de ***PyHome***, que se encarga de la ejecución de la funcionalidad de control de acceso.

Este módulo está diseñado para ser ejecutado sobre una unidad *Raspberri Pi Zero*, por lo que no tiene disponible las 
interfaces de red WiFi ni BlueTooth. Sin embargo, para su desarrollo, si se ha utilizado la versión HW, para un mejor 
*debug*. 

Está compuesto por un módulo ZigBee, para la comunicación con el Centro de Cálculo Primario. 

Código para la implementación de un control de acceso sobre una RPi Zero

https://es.pinout.xyz/resources/raspberry-pi-pinout.png

## XBee
Por facilidad de configuración, se ha decidido que la manera de comunicarse con la antena de **XBee** sea mediante el 
puerto UBS del arduino. 

Para ello, hay que comprobar que tenemos instalado el paquete *usbutils*
~~~
$ dpkg --get-selections | grep usbutils
~~~
## Inicio
El sistema se arranca ejecutando el *__main__.py* del paquete principal con el argumento adecuado, 
atendiendo al entrono de desarrollo que se vaya a emplear.

~~~
Zero@PyHome: $ python3 __main__.py -h
usage: __main__.py [-h] [-R REMOTE]

optional arguments:
  -h, --help            show this help message and exit
  -R REMOTE, --remote REMOTE
                        Defino que tipo de ejecución se va a realizar, remota
                        o local, True o False, respectivamente

~~~