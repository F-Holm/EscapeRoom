import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self, rows, buttons_per_row, row_texts):
        super().__init__()
        self.title("Interfaz Gráfica")
        self.fullscreen = False
        self.geometry("800x600")  # Tamaño inicial de la ventana
        
        self.bind("<F11>", self.toggle_fullscreen)
        
        # Configuración de la columna izquierda
        self.left_frame = tk.Frame(self, width=100, bg='lightgrey')
        self.left_frame.pack(side='left', fill='y')
        
        self.left_label = tk.Label(self.left_frame, text="Texto en la columna izquierda", bg='lightgrey')
        self.left_label.pack(fill='both', expand=True)
        
        # Configuración del área principal
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side='left', fill='both', expand=True)
        
        # Crear filas y botones
        for i in range(rows):
            row_frame = tk.Frame(self.main_frame)
            row_frame.pack(fill='x', expand=True)
            
            # Texto en la parte superior de cada fila
            row_label = tk.Label(row_frame, text=row_texts[i])
            row_label.pack(fill='x')
            
            for j in range(buttons_per_row[i]):
                button_text = f"Botón {i+1}-{j+1}\nCtrl+{j+1}"
                button = tk.Button(row_frame, text=button_text, command=lambda i=i, j=j, text=button_text: self.button_action(i, j, text))
                button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
            
            # Línea divisoria entre filas
            if i < rows - 1:
                separator = ttk.Separator(self.main_frame, orient='horizontal')
                separator.pack(fill='x', pady=5)
        
        # Switch en la parte superior derecha de la segunda fila
        if rows > 1:
            switch_frame = tk.Frame(self.main_frame)
            switch_frame.pack(fill='x')
            switch = tk.Checkbutton(switch_frame, text="Switch")
            switch.pack(side='right')
        
        # Línea divisoria entre la columna izquierda y el área principal
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side='left', fill='y')
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return "break"
    
    def button_action(self, row, col, text):
        if row == 0:  # Solo para botones de la primera fila
            self.show_confirmation_dialog(text)
        else:
            print(f"Botón {row+1}-{col+1} presionado")
    
    def show_confirmation_dialog(self, text):
        response = messagebox.askquestion("Confirmación", f"¿Seguro que quieres {text}?")
        if response == 'yes':
            print(f"Confirmado: {text}")
        else:
            print("Cancelado")

if __name__ == "__main__":
    rows = 3  # Número de filas
    buttons_per_row = [3, 2, 4]  # Número de botones por fila
    row_texts = ["Texto de la fila 1", "Texto de la fila 2", "Texto de la fila 3"]  # Texto en la parte superior de cada fila
    app = App(rows, buttons_per_row, row_texts)
    app.mainloop()
