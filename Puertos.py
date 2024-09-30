from enum import Enum
from Codigos import Codigos
import serial

arduino0 = '/dev/ttyUSB0'
arduino1 = '/dev/ttyUSB1'
arduino2 = '/dev/ttyUSB2'

IRA_ARDUINO = None
BOTON_RFID_ARDUINO = None
LEDS_ARDUINO = None

ira = None
boton_rfid = None
leds = None

def identificar(arduino, puerto):
    arduino.write(Codigos.IDENTIFICATE.value)
    respuesta = None
    while arduino.in_waiting <= 0:
        pass
    respuesta = arduino.readline()
    if (int(respuesta) == ord(Codigos.IRA_IDENTIFICACION.value)):
        ira = puerto
        IRA_ARDUINO = arduino
    elif (int(respuesta) == ord(Codigos.BOTON_RFID_IDENTIFICACION.value)):
        boton_rfid = puerto
        BOTON_RFID_ARDUINO = arduino
    elif (int(respuesta) == ord(Codigos.LEDS_IDENTIFICACION.value)):
        leds = puerto
        LEDS_ARDUINO = arduino

#identificar(serial.Serial(arduino0, 9600, timeout=1), arduino0)
#identificar(serial.Serial(arduino1, 9600, timeout=1), arduino1)
#identificar(serial.Serial(arduino2, 9600, timeout=1), arduino2)

class Puertos(Enum):
    IP_TRIVIA = '192.168.1.10'
    PUERTO_TRIVIA = 8080
    IRA = ira
    LEDS = leds
    BOTON_RFID = boton_rfid