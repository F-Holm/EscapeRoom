from enum import Enum

class Puertos(Enum):
    IRA = '/dev/ttyUSB0'
    LEDS_RGB = '/dev/ttyUSB0'
    IP_TRIVIA = '192.168.0.2'
    PUERTO_TRIVIA = 8080