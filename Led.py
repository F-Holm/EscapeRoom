from enum import Enum
import serial
from Puertos import Puertos, LEDS_ARDUINO

class EfectosLedsRGB(Enum):
    RAYO           = b'\x00' + b'\x00'

class EfectosNeoPixel(Enum):
    CIELO_INFIERNO = b'\x01' + b'\x00'
    CIELO          = b'\x01' + b'\x01'
    RELAMPAGO      = b'\x01' + b'\x02'

class EfectosGlobales(Enum):
    RAYO           = b'\x02' + b'\x00'

class Colores(Enum):
    NEGRO          = b'\x00' + b'\x00' + b'\x00'
    BLANCO         = b'\xFF' + b'\xFF' + b'\xFF'
    ROJO           = b'\xFF' + b'\x00' + b'\x00'
    VERDE          = b'\x00' + b'\xFF' + b'\x00'
    AZUL           = b'\x00' + b'\x00' + b'\xFF'

def cambiarColor(color):
    LEDS_ARDUINO.write(color.value)

def efecto(efecto):
    LEDS_ARDUINO.write(efecto.value)

def closeLED():
    LEDS_ARDUINO.close()