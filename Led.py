from enum import Enum
import serial
from enum import Enum

class Efectos(Enum):
    RAYO = chr(0)

class Colores(Enum):
    ROJO = chr(255) + chr(0) + chr(0)
    VERDE = chr(0) + chr(255) + chr(0)
    AZUL = chr(0) + chr(0) + chr(255)

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def cambiarColor(color):
    arduino.write(color.value)

def efecto(efecto):
    arduino.write(efecto.value)