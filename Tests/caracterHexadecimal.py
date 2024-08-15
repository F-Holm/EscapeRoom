from enum import Enum

class CodigosArduino(Enum):
    START = b'\x00'
    RESTART = b'\x00'
    STOP = b'\x00'
    CLOSE = b'\x00'
    TERMINO = b'\x00'

class Codigos(Enum):
    START = chr(0)
    RESTART = chr(1)
    STOP = chr(2)
    CLOSE = chr(3)
    TERMINO = chr(4)

print(CodigosArduino.START.value == Codigos.START.value)
print(CodigosArduino.START.value == CodigosArduino.START.value)
print(ord(CodigosArduino.START.value))
print(ord(Codigos.START.value))

print(CodigosArduino.START.value + CodigosArduino.START.value == b'\x00'b'\x00')