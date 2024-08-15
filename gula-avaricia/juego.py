from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QDialog,QGridLayout
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QPainter, QImage, QBrush
import sys
import random
import os
import time
import socket
import threading
from enum import Enum

class Codigos(Enum):
    START = chr(0)
    RESTART = chr(1)
    STOP = chr(2)
    CLOSE = chr(3)
    TERMINO = chr(4)


evento = threading.Event()

class MiClase:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexion = None

    def __init__(self):
        self.hilo = threading.Thread(target=self.mi_metodo)
        # Crear un socket TCP/IP
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Obtener la IP privada de la computadora
        hostname = socket.gethostname()
        ip_privada = socket.gethostbyname(hostname)
        # Enlazar el socket a la dirección y puerto
        servidor.bind((ip_privada, 8080))
        # Mostrar la IP privada y el puerto
        print(f"Servidor iniciado en IP: {ip_privada}, Puerto: 8080")
        # Escuchar conexiones entrantes
        servidor.listen(1)
        print("Esperando conexiones...")
        # Aceptar una conexión
        self.conexion, direccion = servidor.accept()
        print(f"Conectado a {direccion}")
    
    def mi_metodo(self):
        #abro Escucha
        while True:
            datos = self.conexion.recv(1024)
            if not datos or datos.decode() == chr(0):
                break
            if ord(datos.decode()) == Codigos.START : #START
                self.start()
            if ord(datos.decode()) == Codigos.STOP : #Terminar pero puede volver a empezar
                self.stop(self.conexion) #arreglar esto
                break
            if ord(datos.decode()) == Codigos.RESTART : #Restart 
                self.stop(self.conexion)
            if ord(datos.decode()) == Codigos.CLOSE : #Temino totalmente el juego 
                self.stop(self.conexion)
                
                
            print(f"Recibido: {ord(datos.decode())}")
    
    def start(self):
        evento.set()
    
    def stop(self): #Arreglar esto 
        self.conexion.close()

    def iniciar_hilo(self):
        self.hilo.start()

        

objeto = MiClase()
objeto.daemon = True
objeto.iniciar_hilo()

evento.wait()
#os.system('sudo vbetool dpms off')
os.system('echo "hola"')

time.sleep(15)
#os.system('sudo vbetool dpms on')
os.system('echo "chau"')

STYLE = "style.css"

def load_stylesheet():
    with open(STYLE, "r") as file:
        return file.read()

class CustomDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(load_stylesheet())
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        
        self.setLayout(layout)

def bienvenida():
    dialog = CustomDialog("¡Bienvenido a la trivia!", "¡Bienvenido a la trivia!\nResponde las siguientes preguntas y gana MUCHISIMAS monedas de chocolate:")
    dialog.exec()

score = 0
easy_correct = 0    
current_question = None

class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer

easy_questions = [
    Question("¿Cuál es la capital de Francia?", ["a) París", "b) Madrid", "c) Roma", "d) Londres"], "a"),
    Question("¿Cuál es una comida tradicional argentina?", ["a) sushi", "b) pizza", "c) asado", "d) hamburguesa"], "c"),
    Question("¿Cuál es el capitán de la selección argentina?", ["a) Di Maria", "b) Messi", "c) Dibu", "d) Paredes"], "b"),
    Question("¿Cuáles son los colores del uniforme del Instituto Politécnico Modelo?", ["a) verde y blanco", "b) rojo y verde", "c) azul y gris", "d) naranja"], "c"),
    Question("¿Quién es el presidente de Argentina actualmente?", ["a) Rodriguez", "b) Perez", "c) Fiore", "d) Milei"], "d"),
    Question("¿Cuánto es 2 + 2?", ["a) 4", "b) 6", "c) 7", "d) 3"], "a"),
    Question("¿Cuál es la capital de Argentina?", ["a) Mendoza", "b) Santa Fe", "c) Buenos Aires", "d) Londres"], "c")
]

hard_questions = [
    Question("¿Cuál es la distancia desde \nBuenos Aires hasta Tokio?", ["a) 17353 km.", "b) 17352 km.", "c) 17354 km.", "d) 17355 km."], "e"),
    Question("¿Cuál es el elemento más abundante\n en la corteza terrestre?", ["a) Hierro", "b) Oxígeno", "c) Hidrogeno", "d) Aluminio"], "h"),
    Question("¿Cuál es la cantidad aproximada de galaxias\n en el universo observable?", ["a) 10^6", "b) 10^8", "c) 10^10", "d) 10^12"], "l"),
    Question("¿Cuál es el resultado de elevar e \n(la base de los logaritmos naturales) a la potencia de pi (π)?", ["a) e^e", "b) π^e", "c) ln(π)", "d) no se puede calcular"], "f"),
    Question("¿Cuál es el valor aproximado de la constante\n de gravitación universal (G) en unidades SI?", ["a) 6.67 x 10^-11 N·m^2/kg^2", "b)9.81 m/s^2", "c) 3.00 x 10^8 m/s", "d) 1.38 x 10^-23 J/K"], "f")
]

dichos = ["La avaricia rompe el saco", "Quien come para vivir, se alimenta;\nque vive para comer, revienta."]

preguntasFacil = easy_questions
preguntasDificil = hard_questions

def glitch_effect(label, original_text):
    glitch_text = ''.join(random.choice(['@', '#', '%', '&', '*', original_text[i]]) for i in range(len(original_text)))
    label.setText(glitch_text)
    QTimer.singleShot(200, lambda: label.setText(original_text))

def verificarRta(answer, question_display, answer_buttons):
    global score
    global easy_correct
    if answer == current_question.correct_answer:
        score += 1
        easy_correct += 1
        msg_box = CustomDialog("Respuesta", "¡Correcto!")
        msg_box.exec()
    elif score > 0 :
        score = 0
        msg_box = CustomDialog("Respuesta", "¡Incorrecto! \n " + random.choice(dichos))
        msg_box.exec()  
    else :
        score = 0
        msg_box = CustomDialog("Respuesta", "¡Incorrecto!")
        msg_box.exec()

    score_msg = CustomDialog("Puntuación", f"Puntuación Total : \n {score} monedas de chocolate.")
    score_msg.exec()
    
    if score != 0:
        seguirJugando()

    if score == 0 and easy_correct >= 2:
        easy_correct = 0
    cargarPregunta(question_display, answer_buttons)

def cargarPregunta(question_display, answer_buttons):
    global current_question

    if easy_correct < 2:
        current_question = random.choice(preguntasFacil)
        preguntasFacil.remove(current_question)
        question_display.setText(current_question.text)
    else:
        current_question = random.choice(preguntasDificil)
        preguntasDificil.remove(current_question)
        question_display.setText(current_question.text)

    for i in range(4):
        answer_buttons[i].setText(current_question.options[i])
        answer_buttons[i].disconnect()
        answer_buttons[i].clicked.connect(lambda _, ans=current_question.options[i][0]: verificarRta(ans, question_display, answer_buttons))

def seguirJugando():
    global seguir
    seguir = QDialog()
    seguir.setWindowTitle("Seguir Jugando")
    seguir.setStyleSheet(load_stylesheet())
    seguir.setWindowFlag(Qt.FramelessWindowHint)
    seguir.showFullScreen()

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    
    seguir.label = QLabel("¡Respondiste muy bien!\n¿Quieres seguir jugando y ganar MÁS monedas de chocolate?")
    seguir.label.setAlignment(Qt.AlignCenter)
    layout.addWidget(seguir.label)
    
    aceptar = QPushButton('Sí')
    denegar = QPushButton('No')
    layout.addWidget(aceptar)
    layout.addWidget(denegar)
    
    seguir.setLayout(layout)
    aceptar.clicked.connect(seguir.close)
    denegar.clicked.connect(ganar)
    
    seguir.exec()

def ganar():
    global score
    mensaje = CustomDialog("¡GANASTE!", f"¡GANASTE!\nFelicidades, elegiste el camino correcto, \n no fuiste avaro, y la gula no te sobrepasó!  \n  Podés ir a buscar {score} monedas!!.")
    mensaje.exec()
    QApplication.quit()

class PasswordDialog(QDialog):
    def __init__(self, correct_password, parent=None):
        super().__init__(parent)
        self.correct_password = correct_password
        self.entered_password = ""
        
        self.setWindowTitle("Ingresar Contraseña")
        self.setStyleSheet(load_stylesheet())
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.display = QHBoxLayout()
        self.layout.addLayout(self.display)

        self.password_labels = []
        for _ in range(4):  # Assuming password length is 4
            label = QLabel("_")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 36px; color: lime; border: 2px solid lime; padding: 10px;")
            self.display.addWidget(label)
            self.password_labels.append(label)

        self.button_grid = QGridLayout()
        self.layout.addLayout(self.button_grid)

        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_clicked)
            self.button_grid.addWidget(button, row, col)

    def button_clicked(self):
        sender = self.sender().text()
        if len(self.entered_password) < 4:
            self.entered_password += sender
            self.update_display()

        if len(self.entered_password) == 4:
            QTimer.singleShot(500, self.check_password)

    def update_display(self):
        for i, label in enumerate(self.password_labels):
            label.setText(self.entered_password[i] if i < len(self.entered_password) else "_")

    def check_password(self):
        if self.entered_password == self.correct_password:
            self.accept()  # Password correct, close dialog
        else:
            self.wrong_password()

    def wrong_password(self):
        self.entered_password = ""
        self.update_display()
        self.flash_red()

    def flash_red(self):
        original_style = self.styleSheet()

        def set_red():
            self.setStyleSheet("QLabel {color: red; border: 2px solid red;} QPushButton {background-color: red; color: black;}")
        
        def set_original():
            self.setStyleSheet(original_style)
        
        def flash():
            set_red()
            QTimer.singleShot(250, set_original)
            QTimer.singleShot(500, set_red)
            QTimer.singleShot(750, set_original)

        flash()


def main():
    global current_question

    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)

    stylesheet = load_stylesheet()
    app.setStyleSheet(stylesheet)

    correct_password = "1234"
    dialog = PasswordDialog(correct_password)
    if dialog.exec() == QDialog.Accepted:
        print("Contraseña correcta, iniciando el juego...")

    bienvenida()

    ventanaPreguntas = QWidget()
    ventanaPreguntas.setWindowTitle("Trivia")
    ventanaPreguntas.setStyleSheet(stylesheet)
    ventanaPreguntas.setWindowFlag(Qt.FramelessWindowHint)
    ventanaPreguntas.showFullScreen()

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    ventanaPreguntas.setLayout(layout)

    question_display = QLabel()
    question_display.setAlignment(Qt.AlignCenter)
    layout.addWidget(question_display)

    buttons_layout = QGridLayout()
    layout.addLayout(buttons_layout)

    answer_buttons = [QPushButton() for _ in range(4)]
    for i, button in enumerate(answer_buttons):
        buttons_layout.addWidget(button, i // 2, i % 2)

    cargarPregunta(question_display, answer_buttons)

    glitch_timer = QTimer()
    glitch_timer.timeout.connect(lambda: glitch_effect(question_display, current_question.text))
    glitch_timer.start(3000)  # Cada 3 segundos se ejecuta el efecto de glitch

    ventanaPreguntas.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
