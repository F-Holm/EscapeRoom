from enum import Enum
import serial
from Puertos import Puertos

class Efectos(Enum):
    RAYO = b'\x00' + b'\x00'

class EfectosNeoPixel(Enum):
    CIELO_INFIERNO = b'\x01' + b'\x00'
    CIELO = b'\x01' + b'\x01'

class Colores(Enum):
    ROJO = b'\xFF' + b'\x00' + b'\x00'
    VERDE = b'\x00' + b'\xFF' + b'\x00'
    AZUL = b'\x00' + b'\x00' + b'\xFF'

arduino = serial.Serial(Puertos.LEDS.value, 9600, timeout=1)

def cambiarColor(color):
    arduino.write(color.value)

def efecto(efecto):
    arduino.write(efecto.value)

def closeLED():
    arduino.close()