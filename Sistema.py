from enum import Enum
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
from time import sleep
from Sonido import reproducirSonido, detenerSonido, delay, closePygame, Sonidos
import serial, time, threading

sistema = None

root = tk.Tk()
root.title("Escape room")

class juegoIra:
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    
    hilo = None
    terminar = threading.Event()
    termino = threading.Event()

    def start(self):
        self.arduino.write(b'0')
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()

    def cerrarHilo(self):
        self.arduino.write(b'1')
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
        sistema.siguienteNivel()
    
    def close(self):
        self.cerrarHilo()
        self.closeArduino()

    def restart(self):
        self.arduino.write(b'2')

    def closeArduino(self):
        self.arduino.close()
    
    def hiloArduino(self):
        while not self.terminar.is_set():
            if self.arduino.in_waiting > 0:
                try:
                    self.arduino.readline().decode('utf-8').strip()  # Decodificar y eliminar saltos de línea
                except Exception as e:
                    print(f"Error leyendo desde el puerto serial: {e}")
                if not self.terminar.is_set():
                    root.after(500, lambda: sistema.siguienteNivel())
                self.terminar.set()
                self.termino.set()

class Sistema:
    niveles = [juegoIra()]#Agregá niveles utilizando las clases correspondientes -> [Nivle1(), Nivle2(), Nivel3("qwerty"), ...]
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
        closePygame()
        closeTTK()
        print("Juego terminado correctamente :)")
        sys.exit()

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

def closeTTK():
    root.quit()
    root.destroy()

root.mainloop()