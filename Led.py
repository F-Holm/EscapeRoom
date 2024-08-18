from enum import Enum
import serial
from Puertos import Puertos

class EfectosLedsRGB(Enum):
    RAYO           = b'\x00' + b'\x00'

class EfectosNeoPixel(Enum):
    CIELO_INFIERNO = b'\x01' + b'\x00'
    CIELO          = b'\x01' + b'\x01'

class EfectosGlobales(Enum):
    RAYO           = b'\x02' + b'\x00'

class Colores(Enum):
    NEGRO          = b'\x00' + b'\x00' + b'\x00'
    BLANCO         = b'\xFF' + b'\xFF' + b'\xFF'
    ROJO           = b'\xFF' + b'\x00' + b'\x00'
    VERDE          = b'\x00' + b'\xFF' + b'\x00'
    AZUL           = b'\x00' + b'\x00' + b'\xFF'

arduino = None

def conectarLEDS():
    global arduino
    arduino = serial.Serial(Puertos.LEDS.value, 9600, timeout=1)

def cambiarColor(color):
    arduino.write(color.value)

def efecto(efecto):
    arduino.write(efecto.value)

def closeLED():
    arduino.close()