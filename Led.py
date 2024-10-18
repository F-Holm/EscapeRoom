from enum import Enum
import serial
from Puertos import Puertos, LEDS_ARDUINO
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

def efecto(efecto):
    LEDS_ARDUINO.write(efecto.value)
    if (efecto == Efectos.LIGHTNING):
        reproducirSonido(Sonidos.TRUENO)

def closeLED():
    if LEDS_ARDUINO != None:
        LEDS_ARDUINO.close()