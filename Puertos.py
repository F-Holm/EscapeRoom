from enum import Enum

class Puertos(Enum):
    IP_TRIVIA = '192.168.1.10'
    PUERTO_TRIVIA = 8080
    LEDS = '/dev/ttyUSB0'
    BOTON_RFID = '/dev/ttyUSB1'
    IRA = '/dev/ttyUSB2'