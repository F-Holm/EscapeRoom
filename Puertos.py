from enum import Enum
from Codigos import Codigos
import serial

LEDS_ARDUINO = None
BOTON_RFID_ARDUINO = None
IRA_ARDUINO = None

class Puertos(Enum):
    IP_TRIVIA = '192.168.1.10'
    PUERTO_TRIVIA = 8080
    LEDS = '/dev/ttyUSB0'
    BOTON_RFID = '/dev/ttyUSB1'
    IRA = '/dev/ttyUSB2'

LEDS_ARDUINO = serial.Serial(Puertos.LEDS.value, 9600, timeout=1)
BOTON_RFID_ARDUINO = serial.Serial(Puertos.BOTON_RFID.value, 9600, timeout=1)
IRA_ARDUINO = serial.Serial(Puertos.IRA.value, 9600, timeout=1)