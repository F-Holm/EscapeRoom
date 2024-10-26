from enum import Enum
import serial
from Puertos import Puertos
from Sonido import Sonidos, detenerTodosLosSonidos, toggleSonido, closePygame, iniciarPygame, reproduciendo, reproducirSonido, detenerSonido

class Efectos(Enum):
    APAGADO = b'\x00'
    CONFETTI = b'\x01'
    LIGHTNING = b'\x02'
    CIERRE = b'\x03'
    ENCENDIDO_GRADUAL = b'\x04'
    BLANCO = b'\x05'
    PERDISTE = b'\x06'
    ROJO = b'\x07'

    AGUA = b'\x43'

arduino = None

def conectarArduinoLeds():
    try:
        global arduino
        arduino = serial.Serial(Puertos.LEDS, 9600, timeout=1)
    except Exception as e:
        arduino = None
        print("Error conexión: Leds")

def efecto(efecto):
    if arduino != None:
        arduino.write(efecto.value)
        if (efecto == Efectos.LIGHTNING):
            reproducirSonido(Sonidos.TRUENO)

def closeLED():
    if arduino != None:
        arduino.close()