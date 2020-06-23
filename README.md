# Zero-Project
___
***Zero-Project***, es el módulo de ***PyHome***, que se encarga de la ejecución de la funcionalidad de control de acceso.

Este módulo, está diseñado para ser ejecutado sobre una unidad *Raspberri Pi Zero*, por lo que no se tienen en cuenta las 
interfaces de red WiFi ni bluetooth. (*Sin embargo, para su desarrollo, si se ha utilizado la versión HW, para un mejor 
*debug**).  

## Estructura
~~~
├── config
│   ├── __init__.py
├── env.ini
├── local.ini
├── __main__.py
├── README.md
├── requirements.txt
├── Scripts
│   ├── router.xml
│   └── run.sh
├── setup.py
├── test
│   ├── __init__.py
│   └── servo.py
└── watchDog
    ├── __init__.py
    ├── servo.py
    ├── watchDog.py
    └── xbee.py 
~~~

## Componentes
Toda la estructura se asienta sobre el objeto ```watchDog.watchDog.WatchDog```, que será el que integre cada uno del
resto de componentes que vaya a disponer el dispositivo.

La interface de comunicación con el módulo central ***PyHome*** o **Centro de Cálculo Primario** (*CPP*), se realiza a 
través de una antena **XBee(*ZigBee*)**.

La parte mecánica que realizará la metáfora de pasar las vueltas de la cerradura, será implementada en un servo.

https://es.pinout.xyz/resources/raspberry-pi-pinout.png

### XBee
Por facilidad de configuración, se ha decidido que la manera de comunicarse con la antena de **XBee** sea mediante el 
puerto UBS del arduino. 

Para ello, hay que comprobar que tenemos instalado el paquete *usbutils*
~~~
$ dpkg --get-selections | grep usbutils
~~~

El sistema escaneará los disitivos USB conectados y tratara de crear la conexíon mediante un objeto *ZigBeeDevice* de la
librería *digi* (https://xbplib.readthedocs.io/en/stable/api/modules.html).

### Servo
El dispositivo empleado para este fin es el servo ```SG90```.  

Para su control, se ha empleado ```gpiozero.output_devices.AngularServo```, que es heredado por la clase 
```watchDog.servo.Cerradura```.    
Esta es invocada con la llamada:  
```python
    def __init__(self, pin=None, pin_factory=None):
...
    super(Cerradura, self).__init__(pin, 90, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH, SPEED,
                                        pin_factory=pin_factory)
...
```  
donde:
```python
MIN_PULSE_WIDTH = 35 / 100000  # 0.35ms
MAX_PULSE_WIDTH = 200 / 100000  # 2ms
SPEED = 20 / 1000  # 20ms corresponde con la frecuencia del SG90
SLEEP_TIME = 0.2
```
La conexión al pin de control se ha configurado en el pin *12* - *GPIO18* 

## Lector RFID
Para realizar la identificación del usuario, se empleará un lector del tarjetas RFID. Para esta demostración se empleará
 el dispositivo RFID-RC522.  
Para usar un dispositivo de este tipo, es necesario activar la interface de la RPi para SPI, para ello lanzamos el comando:  
 ~~~bash 
$ sudo raspi-config
~~~ 
Navegamos hasta la opción *5 Interfacing Options* / *P4 SPI*, y aceptamos que queremos usar esa interface.  
Tras aplicar los cambios, será necesario reiniciar el sistema:
~~~bash
$ sudo reboot
~~~
Podemos comprobar que se han realizado correctamente los cambios con el comando:
~~~bash
$ lsmod | grep spi_bcm2835
~~~
Tras lo que, si todo ha ido bien, deberíamos obtener algún resultado.

### RFID-RC522

Esta clase realiza una encapsulación/abstracción de la libreria  *mfrc522* de https://pimylifeup.com/raspberry-pi-rfid-rc522/, con la configuración estandar, es decir:  

| RC522 PIN | RPi Zero PIN Number | RPi Zero PIN Name |
|-----------|---------------------|-------------------|
| SDA       | 24                  | GPIO8             |
| SCK       | 23                  | GPIO11            |
| MOSI      | 19                  | GPIO10            |
| MISO      | 21                  | GPIO9             |
| RST       | 22                  | GPIO25            |
| GND       | GND                 |                   |
| PWD       | 3.3V                |                   |

## Inicio
El sistema se arranca ejecutando el *__main__.py* del paquete principal con el argumento adecuado, 
atendiendo al entrono de desarrollo que se vaya a emplear.

~~~python
Zero@PyHome: $ python3 __main__.py -h
usage: __main__.py [-h] [-R REMOTE]

optional arguments:
  -h, --help            show this help message and exit
  -R REMOTE, --remote REMOTE
                        Defino que tipo de ejecución se va a realizar, remota
                        o local, True o False, respectivamente
~~~

Tras iniciar el proceso, el sistema cargará la configuración de los ficheros ***env.ini*** y ***local.ini***.  

Después, el sistema creará los elementos que precise, a saber: LED, Servo, antena ZigBee y antena RFID. Si todo ha sido 
correcto, mostrá un log similar al siguiente:  

~~~log
Leyendo configuración ...
Ficheros a tratar:      ['env.ini', 'local.ini']
Se han recibido los ficheros
Configurador de propiedades cargado
Preparandose para tratar el fichero:    env.ini
        Extrayendo configuración del fichero:   env.ini
Preparandose para tratar el fichero:    local.ini
        Extrayendo configuración del fichero:   local.ini
Configuración recuperada correctamente.

Inicializando WatchDog
        Modo Local:     True
Cargando configuración para ejecución en local.

Creando la cerradura
Cerradura correcta

Creando la antena
Puertos encontrados: ['/dev/ttyUSB0']
Frecuencia de trabajo: 9600
Enlace remoto: 0013A2004151####
Probando el puerto: /dev/ttyUSB0
        Conectada la antena 'Arduino Router(0013A2004151####)' al puerto /dev/ttyUSB0

Inicialización de WacthDog correcta

Stapleton se ha despertado.
~~~

Una vez el sistema se haya cargado, mandará una señal al CPD para indicarle que está disponible y entrará en un bucle en
el que, a cada ciclo, comprobará si se ha recibido un mensaje desde el CPD o si se ha detectado una tarjeta RFID, hasta 
que reciba la señal de apagado de ese, que desencadenará las acciones necesarias para asegurarse que los elementos
empleados están desconectados.



 ### ENV.INI
 Este fichero está dstino a almacenar la información que el sistema necesita para funcionar, como lugares GPIO donde se
 pincharán los diversos elementos, o información general del sistema.
 
 ### LOCAL.INI
 Este fichero contiene la información privada del sistema, como contraseñas, direcciones ip o mac, ... por lo que no se 
 incluye en el repositorio.
