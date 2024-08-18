import sys
from Sonido import closePygame, iniciarPygame
from Led import closeLED, conectarLEDS
from JuegoIra import JuegoIra
from JuegoTrivia import JuegoTrivia
from variablesGlobales import sistema, root

class Sistema:
    niveles = None
    nivelActual = 0

    def __init__(self):#Juegos: JuegoIra(), JuegoTrivia()
        self.niveles = []#Agregá niveles utilizando las clases correspondientes -> [Nivle1(), Nivle2(), Nivel3("qwerty"), ...]

    def start(self):
        self.niveles[self.nivelActual].start()

    def stop(self):
        self.niveles[self.nivelActual].stop()

    def restart(self):
        self.niveles[self.nivelActual].restart()

    def nivelAnterior(self):
        if self.nivelActual != 0:
            self.stop()
            self.nivelActual -= 1
            self.start()
        else:
            self.restart()

    def siguienteNivel(self):
        if self.nivelActual != len(self.niveles) - 1:
            self.stop()
            self.nivelActual += 1
            self.start()
        else:
            self.stop()()
            self.nivelActual = 0
    
    def reiniciarJuego(self):
        self.stop()
        self.nivelActual = 0
        self.start
    
    def terminarJuego(self):
        for nivel in self.niveles:
            nivel.close()
        closeLED()
        closePygame()
        closeTTK()
        sys.exit()

def closeTTK():
    root.quit()
    root.destroy()

def iniciarSistema():
    global sistema
    sistema = Sistema()
    conectarLEDS()
    iniciarPygame()