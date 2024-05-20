from Constantes import Sonidos
import pygame
from time import sleep

pygame.init()

def reproducirSonido(sonido, loop):#enum sonido, bool loop
    pygame.mixer.music.load(sonido.value)
    if loop:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()

def detenerSonidos():
    pygame.mixer.music.stop()

def delay(segundos):
    sleep(segundos)