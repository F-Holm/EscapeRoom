from enum import Enum
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
from time import sleep
from Sonido import reproducirSonido, detenerSonido, delay, closePygame, Sonidos
import serial, time, threading
import socket
from Led import cambiarColor, efecto, Efectos, Colores, closeLED, EfectosNeoPixel
from Codigos import Codigos
from Puertos import Puertos
from JuegoIra import JuegoIra
from JuegoTrivia import JuegoTrivia

sistema = None

root = tk.Tk()
root.title("Escape room")

class Sistema:#Juegos: JuegoIra(), JuegoTrivia()
    niveles = [JuegoIra()]#Agregá niveles utilizando las clases correspondientes -> [Nivle1(), Nivle2(), Nivel3("qwerty"), ...]
    nivelActual = 0

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
            self.terminarJuego()
    
    def terminarJuego(self):
        for nivel in self.niveles:
            nivel.close()
        closeLED()
        closePygame()
        closeTTK()
        print("Juego terminado correctamente :)")
        sys.exit()

def closeTTK():
    root.quit()
    root.destroy()

sistema = Sistema()

juegoAnterior = ttk.Button(root, text="Nivel anterior\n<--", command=sistema.nivelAnterior)
juegoAnterior.grid(row=0, column=0, padx=10, pady=10)
root.bind("<KeyPress-Left>", lambda e: sistema.nivelAnterior())

juegoSiguiente = ttk.Button(root, text="Siguiente nivel\n-->", command=sistema.siguienteNivel)
juegoSiguiente.grid(row=0, column=2, padx=10, pady=10)
root.bind("<KeyPress-Right>", lambda e: sistema.siguienteNivel())

juegoSiguiente = ttk.Button(root, text="Iniciar nivel\narriba", command=sistema.start)
juegoSiguiente.grid(row=1, column=0, padx=10, pady=10)
root.bind("<KeyPress-Up>", lambda e: sistema.start())

juegoSiguiente = ttk.Button(root, text="Detener nivel\nabajo", command=sistema.stop)
juegoSiguiente.grid(row=1, column=2, padx=10, pady=10)
root.bind("<KeyPress-Down>", lambda e: sistema.stop())

juegoSiguiente = ttk.Button(root, text="Reiniciar nivel\nenter", command=sistema.restart)
juegoSiguiente.grid(row=1, column=1, padx=10, pady=10)
root.bind("<Return>", lambda e: sistema.restart())

juegoSiguiente = ttk.Button(root, text="Terminar juego\nescape", command=sistema.terminarJuego)
juegoSiguiente.grid(row=2, column=1, padx=10, pady=10)
root.bind("<Escape>", lambda e: sistema.terminarJuego())

#Efectos RGB

juegoSiguiente = ttk.Button(root, text="Rayo\nq", command=lambda: efecto(Efectos.RAYO))
juegoSiguiente.grid(row=3, column=0, padx=10, pady=10)
root.bind("<KeyPress-q>", lambda e: efecto(Efectos.RAYO))

#Colores RGB

juegoSiguiente = ttk.Button(root, text="rojo\na", command=lambda: cambiarColor(Colores.ROJO))
juegoSiguiente.grid(row=4, column=0, padx=10, pady=10)
root.bind("<KeyPress-a>", lambda e: cambiarColor(Colores.ROJO))

juegoSiguiente = ttk.Button(root, text="verde\ns", command=lambda: cambiarColor(Colores.VERDE))
juegoSiguiente.grid(row=4, column=1, padx=10, pady=10)
root.bind("<KeyPress-s>", lambda e: cambiarColor(Colores.VERDE))

juegoSiguiente = ttk.Button(root, text="azul\nd", command=lambda: cambiarColor(Colores.AZUL))
juegoSiguiente.grid(row=4, column=2, padx=10, pady=10)
root.bind("<KeyPress-d>", lambda e: cambiarColor(Colores.AZUL))

#Efectos neo pixel

juegoSiguiente = ttk.Button(root, text="cielo infierno\nz", command=lambda: efecto(EfectosNeoPixel.CIELO_INFIERNO))
juegoSiguiente.grid(row=5, column=0, padx=10, pady=10)
root.bind("<KeyPress-z>", lambda e: efecto(EfectosNeoPixel.CIELO_INFIERNO))

juegoSiguiente = ttk.Button(root, text="cielo\nx", command=lambda: efecto(EfectosNeoPixel.CIELO))
juegoSiguiente.grid(row=5, column=1, padx=10, pady=10)
root.bind("<KeyPress-x>", lambda e: efecto(EfectosNeoPixel.CIELO))

root.mainloop()