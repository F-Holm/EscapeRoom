from enum import Enum

class Codigos(Enum):
    START = b'\x00'      # Inicia el juego
    RESTART = b'\x01'    # Reinicia el juego
    STOP = b'\x02'       # Detiene el juego pero puede volver a iniciarse
    CLOSE = b'\x03'      # Detiene el juego y no puede volver a iniciarse
    TERMINO = b'\x04'    # Indica que el juego terminó. Esto se manda desde el juego al sistema
    START_BOTON = b'\x05'# Indica que debe iniciarse el juego del botón