import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Sonido import reproducirSonido, detenerSonido, delay, closePygame, Sonidos, detenerTodosLosSonidos, toggleSonido
from Led import cambiarColor, efecto, EfectosLedsRGB, Colores, closeLED, EfectosNeoPixel, conectarLEDS, EfectosGlobales
from Codigos import Codigos
from Puertos import Puertos
from JuegoIra import JuegoIra
from JuegoTrivia import JuegoTrivia
from variablesGlobales import sistema, root
from Sistema import iniciarSistema

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Escape Room")
        self.fullscreen = False
        self.geometry("800x600")
        
        self.bind("<F11>", self.toggle_fullscreen)
        
        self.configurarColumnaIzquierda()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side='left', fill='both', expand=True)
        
        self.escaperoom()
        self.nivelActual()
        self.efectosGlobales()
        self.efectosNeoPixel()
        self.efectosLedsRGB()
        self.coloresLedsRGB()
        self.sonidos()
        
        #self.crearSwitch()
        self.separadorVertical()
    
    def separadorVertical(self):
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side='left', fill='y')
    
    def configurarColumnaIzquierda(self):
        self.left_frame = tk.Frame(self, width=100, bg='lightgrey')
        self.left_frame.pack(side='left', fill='y')
        
        self.left_label = tk.Label(self.left_frame, text="Texto en la columna izquierda", bg='lightgrey')
        self.left_label.pack(fill='both', expand=True)
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return "break"
    
    def show_confirmation_dialog(self, accion):
        text = ""
        if accion == 0:
            text = "iniciar el juego"
        elif accion == 1:
            text = "volver al nivel anterior"
        elif accion == 2:
            text = "ir al siguiente nivel"
        elif accion == 3:
            text = "reiniciar el juego"
        elif accion == 4:
            text = "terminar el juego"
        else:
            return
        
        response = messagebox.askquestion("Confirmación", f"¿Seguro que quieres {text}?")
        if response == 'yes':
            if accion == 0:
                iniciarSistema()
            elif accion == 1:
                sistema.nivelAnterior()
            elif accion == 2:
                sistema.siguienteNivel()
            elif accion == 3:
                sistema.reiniciarJuego()
            elif accion == 3:
                sistema.terminarJuego()

    def crearSwitch(self):
        switch_frame = tk.Frame(self.main_frame)
        switch_frame.pack(fill='x')
        switch = tk.Checkbutton(switch_frame, text="Switch")
        switch.pack(side='right')
    
    def separadorHorizontal(self):
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
    
    def update_left_text(self, texto):
        self.left_label.config(text=texto)
    
    def escaperoom(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Escape Room")
        row_label.pack(fill='x')
        
        button_text = "Iniciar Escape Room"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(0))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Nivel Anterior"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(1))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Siguiente Nivel"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(2))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Reiniciar Escape Room"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(3))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Terminar Escape Room"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(4))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def nivelActual(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Nivel Actual")
        row_label.pack(fill='x')
        
        button_text = "Iniciar Nivel"
        button = tk.Button(row_frame, text=button_text, command=sistema.start)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Reiniciar Nivel"
        button = tk.Button(row_frame, text=button_text, command=sistema.restart)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Detener Nivel"
        button = tk.Button(row_frame, text=button_text, command=sistema.stop)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def efectosGlobales(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Efectos Globales")
        row_label.pack(fill='x')
        
        button_text = "Rayo"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(EfectosGlobales.RAYO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def efectosNeoPixel(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Efectos Neo Pixel")
        row_label.pack(fill='x')
        
        button_text = "Cielo Infierno"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(EfectosNeoPixel.CIELO_INFIERNO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Cielo"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(EfectosNeoPixel.CIELO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def efectosLedsRGB(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Efectos LEDs RGB")
        row_label.pack(fill='x')
        
        button_text = "Rayo"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(EfectosLedsRGB.RAYO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def coloresLedsRGB(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Colores LEDs")
        row_label.pack(fill='x')
        
        button_text = "Negro"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.NEGRO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Blanco"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.BLANCO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Rojo"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.ROJO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Verde"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.VERDE))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Azul"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.AZUL))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def sonidos(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Sonidos")
        row_label.pack(fill='x')

        button_text = "Detener todos los sonidos"
        button = tk.Button(row_frame, text=button_text, command=detenerTodosLosSonidos)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Himno de la URSS"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.HIMNO_URSS))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "JIJIJIJA"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.JIJIJIJA))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        #self.separadorHorizontal()

    def actualizarNivel(self):
        pass


if __name__ == "__main__":
    root = App()
    root.mainloop()
