# Zero-Project
___
***Zero-Project***, es el módulo de ***PyHome***, que se encarga de la ejecución de la funcionalidad de control de acceso.

Este módulo, está diseñado para ser ejecutado sobre una unidad *Raspberri Pi Zero*, por lo que no se tienen en cuenta las 
interfaces de red WiFi ni BlueTooth. (*Sin embargo, para su desarrollo, si se ha utilizado la versión HW, para un mejor 
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