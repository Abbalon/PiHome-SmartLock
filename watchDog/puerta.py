from digi.xbee.devices import ZigBeeDevice
from gpiozero import Servo, LED
from gpiozero.pins.pigpio import PiGPIOFactory

import setup

# Definición de variables
sg90 = None
ok_led = None
warn_led = None
error_led = None
monitor_led = None

# Configuración condicional atendiendo a si el código se ejecuta en local
# o desde otra máquina
if setup.remote:
    factory = PiGPIOFactory(host=setup.remote_host)
    # Seteamos el pin de datos del servo  un puerto PWM
    servo = Servo(setup.pin_servo, pin_factory=factory)
    # Seteo de los pines
    ok_led = LED(setup.pin_success, pin_factory=factory)
    warn_led = LED(setup.pin_warn, pin_factory=factory)
    error_led = LED(setup.pin_error, pin_factory=factory)
    monitor_led = LED(setup.pin_monitor, pin_factory=factory)
else:
    # Seteamos el pin de datos del servo  un puerto PWM
    servo = Servo(setup.pin_servo)
    # Seteo de los pines
    ok_led = LED(setup.pin_success)
    warn_led = LED(setup.pin_warn)
    error_led = LED(setup.pin_error)
    monitor_led = LED(setup.pin_monitor)

# Configuramos la antena Xbee
xbee = ZigBeeDevice(setup.xbee_route, setup.xbee_baudrate)
