import pygame
from enum import Enum

class Sonido:
    def __init__(self, sonido, loop, canal, volumen):
        self.sonido = sonido
        self.loop = loop
        self.canal = canal
        self.volumen = volumen #de 0.0 a 1.0

class Sonidos(Enum):
    RISA_DIABOLICA = Sonido("Sonidos/risaDiabolica.mp3", 0, 0, 1.0)
    GRITO = Sonido("Sonidos/grito.mp3", 0, 1, 1.0)
    DESPERTADOR = Sonido("Sonidos/despertadorSamsung.mp3", 1, 2, 1.0)
    TRUENO = Sonido("Sonidos/trueno.mp3", 0, 3, 1.0)
    MUSICA_FONDO = Sonido("Sonidos/musicaFondo.mp3", 1, 4, 1.0)
    
    GANASTE = Sonido("Sonidos/ganaste.m4a", 0, 5, 1.0)
    HORA = Sonido("Sonidos/hora.m4a", 0, 6, 1.0)
    PERDISTE = Sonido("Sonidos/perdiste.m4a", 0, 7, 1.0)
    RISA_MALA = Sonido("Sonidos/risa_mala.m4a", 0, 8, 1.0)
    RISA_MALA_2 = Sonido("Sonidos/risa_mala_2.m4a", 0, 9, 1.0)
    TEXTO_MAS_LENTO = Sonido("Sonidos/texto_mas_lento.m4a", 0, 10, 1.0)

CANTIDAD_CANALES = 11

def iniciarPygame():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(CANTIDAD_CANALES)

def reproducirSonido(sonido):
    canal = pygame.mixer.Channel(sonido.value.canal)
    canal.set_volume(sonido.value.volumen)
    if sonido.value.loop:
        canal.play(pygame.mixer.Sound(sonido.value.sonido), -1)
    else:
        canal.play(pygame.mixer.Sound(sonido.value.sonido))

def detenerSonido(sonido):
    canal = pygame.mixer.Channel(sonido.value.canal)
    if (canal.get_busy()):
        canal.stop()

def detenerTodosLosSonidos():
    for i in range(CANTIDAD_CANALES):
        canal = pygame.mixer.Channel(i)
        if (canal.get_busy()):
            canal.stop()

def reproduciendo(sonido):
    return pygame.mixer.Channel(sonido.value.canal).get_busy()

def toggleSonido(sonido):
    canal = pygame.mixer.Channel(sonido.value.canal)
    if canal.get_busy():
        canal.stop()
    else:
        reproducirSonido(sonido)

def closePygame():
    pygame.quit()
