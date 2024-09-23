from enum import Enum

class CodigosArduino(Enum):
    START = b'\x00'
    RESTART = b'\x00'
    STOP = b'\x00'
    CLOSE = b'\x00'
    TERMINO = b'\x00'

class Codigos(Enum):
    START = b'\x00' # Inicia el juego
    RESTART = b'\x01' # Reinicia el juego
    STOP = b'\x02' # Detiene el juego pero puede volver a iniciarse
    CLOSE = b'\x03' # Detiene el juego y no puede volver a iniciarse
    TERMINO = b'\x04' # Indica que el juego terminó. Esto se manda desde el juego al sistema
    
    BOTON_START = b'\xA0' # Indica que debe iniciarse el juego del botón
    BOTON_RESTART = b'\xA1' # Indica que debe reiniciarse el juego del botón
    BOTON_STOP = b'\xA2' # Indica que debe terminarse el juego del botón
    BOTON_TERMINO = b'\xA3' # Indica que terminó el juego del botón. Esto se manda desde el juego al sistema
    
    IRA_JUGANDO = b'\xB0'
    IRA_PERDIERON = b'\xB1'
    IRA_TERMINO_JUGADOR_1 = b'\xB2'
    IRA_TERMINO_JUGADOR_2 = b'\xB3'
    
    RFID_0_PAREJAS = b'\xC0' # Cuantas parejas correctas hay
    RFID_1_PAREJAS = b'\xC1'
    RFID_2_PAREJAS = b'\xC2'
    RFID_3_PAREJAS = b'\xC3'
    RFID_4_PAREJAS = b'\xC4'
    
    TRIVIA_0_MONEDAS = b'\xD0' # Cuantas monedas le deberíamos dar
    TRIVIA_1_MONEDAS = b'\xD1'
    TRIVIA_2_MONEDAS = b'\xD2'
    TRIVIA_3_MONEDAS = b'\xD3'
    TRIVIA_4_MONEDAS = b'\xD4'
    
    TRIVIA_PREGUNTA_1 = b'\xDA' # En que pregunta está
    TRIVIA_PREGUNTA_2 = b'\xDB'
    TRIVIA_PREGUNTA_3 = b'\xDC'
    TRIVIA_PREGUNTA_4 = b'\xDD'
    TRIVIA_PREGUNTA_5 = b'\xDE'

print(ord(Codigos.TRIVIA_PREGUNTA_5.value) == int("222"))