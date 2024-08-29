from enum import Enum

class Codigos(Enum):
    START = b'\x00'        # Inicia el juego
    RESTART = b'\x01'      # Reinicia el juego
    STOP = b'\x02'         # Detiene el juego pero puede volver a iniciarse
    CLOSE = b'\x03'        # Detiene el juego y no puede volver a iniciarse
    TERMINO = b'\x04'      # Indica que el juego terminó. Esto se manda desde el juego al sistema
    START_BOTON = b'\x05'  # Indica que debe iniciarse el juego del botón
    RESTART_BOTON = b'\x06'# Indica que debe reiniciarse el juego del botón
    STOP_BOTON = b'\x07'   # Indica que debe terminarse el juego del botón
    TERMINO_BOTON = b'\x08'# Indica que terminó el juego del botón. Esto se manda desde el juego al sistema