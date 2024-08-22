import pygame
from enum import Enum

class Sonidos_(Enum):
    HIMNO_URSS = "Sonidos/Himno nacional de la Unión de Repúblicas Socialistas Soviéticas.mp3"
    JIJIJIJA = "Sonidos/JIJIJIJA.mp3"

print(Sonidos_.JIJIJIJA.name)