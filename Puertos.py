from enum import Enum

class Puertos(Enum):
    IRA = '/dev/ttyUSB0'
    LEDS = '/dev/ttyUSB0'
    IP_TRIVIA = '192.168.1.10'
    PUERTO_TRIVIA = 8080
    BOTON_RFID = '/dev/ttyUSB0'