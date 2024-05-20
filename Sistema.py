import Constantes
from Constantes import Sonidos
import MetodosComunes

class Sistema:
    niveles = []#Agregá niveles utilizando las clases hijas -> [Nivle1(), Nivle2(), Nivel3("qwerty"), ...]
    nivelActual = 0

    def start():
        MetodosComunes.reproducirSonido(Sonidos.HIMNO_URSS, 0)
        MetodosComunes.reproducirSonido(Sonidos.JIJIJIJA, 1)

    def stop():
        MetodosComunes.detenerSonidos()

    def restart():
        pass

    def nivelAnterior(self):
        if self.nivelActual != 0:
            nivelActual -= 1

    def siguienteNivel(self):
        if self.nivelActual != len(self.niveles) - 1:
            self.nivelActual += 1
    
while 1:

    sistema = Sistema()
    sistema.start()
    MetodosComunes.delay(4)
    sistema.stop()
    #nivel0
    #nivle1
    #nivle2