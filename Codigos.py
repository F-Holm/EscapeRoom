from enum import Enum

class CodigosArduino(Enum):
    START = b'\x00'
    RESTART = b'\x01'
    STOP = b'\x02'
    CLOSE = b'\x03'
    TERMINO = b'\x04'

class Codigos(Enum):
    START = chr(0)
    RESTART = chr(1)
    STOP = chr(2)
    CLOSE = chr(3)
    TERMINO = chr(4)