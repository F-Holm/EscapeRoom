import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
import random

score = 0
easy_correct = 0
current_question = None
signal_connections = []  # Lista para almacenar las conexiones de señales
app = None  # Variable global para la aplicación

class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer

def main():
    global current_question
    global app
    
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Trivia")
    window.setGeometry(100, 100, 500, 300)  # Ajustar geometría de la ventana

    layout = QVBoxLayout()
    window.setLayout(layout)

    question_label = QLabel("¡Bienvenido a la trivia! Responde las siguientes preguntas y gana monedas de chocolate:")
    layout.addWidget(question_label)

    question_display = QLabel()
    layout.addWidget(question_display)

    buttons_layout = QVBoxLayout()

    answer_buttons = []
    for i in range(4):
        button = QPushButton()
        buttons_layout.addWidget(button)
        answer_buttons.append(button)

    layout.addLayout(buttons_layout)

    window.show()
    next_question(question_display, answer_buttons)
    sys.exit(app.exec_())

def check_answer(answer, question_display, answer_buttons):
    global score
    global easy_correct
    
    if answer == current_question.correct_answer:
        score += 1
        easy_correct += 1
        QMessageBox.information(None, "Respuesta", "¡Correcto!")
    else:
        score = 0
        QMessageBox.critical(None, "Respuesta", "¡Incorrecto!")
    
    QMessageBox.information(None, "Puntuación", f"Tienes {score} monedas de chocolate.")
    
    if easy_correct >= 2:
        reply = QMessageBox.question(None, 'Continuar', '¿Quieres seguir jugando?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            next_question(question_display, answer_buttons, hard=True)
        else:
            QMessageBox.information(None, "Fin del juego", "¡Gracias por jugar!")
            app.quit()
    else:
        next_question(question_display, answer_buttons, hard=False)

def next_question(question_display, answer_buttons, hard=False):
    global current_question
    global signal_connections
    
    if not hard:
        current_question = random.choice(easy_questions)
    else:
        current_question = random.choice(hard_questions)
    
    question_display.setText(current_question.text)
    
    # Actualizar texto de los botones y conectar señales
    for i in range(4):
        answer_buttons[i].setText(current_question.options[i])
        
        # Conectar señales usando una función lambda para capturar el valor correcto de la respuesta
        connection = answer_buttons[i].clicked.connect(lambda _, ans=current_question.options[i][0]: check_answer(ans, question_display, answer_buttons))
        signal_connections.append(connection)

    # Desconectar señales anteriores (si es necesario)
    if len(signal_connections) > 4:
        for connection in signal_connections[:-4]:
            connection.disconnect()
            signal_connections = signal_connections[-4:]

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
    Question("¿Cuál es la distancia desde Buenos Aires hasta Tokio?", ["a) 17353 km.", "b) 17352 km.", "c) 17354 km.", "d) 17355 km."], "b"),
    Question("¿Cuál es el elemento más abundante en la corteza terrestre?", ["a) Hierro", "b) Oxígeno", "c) Hidrogeno", "d) Aluminio"], "b"),
    Question("¿Cuál es la cantidad aproximada de galaxias en el universo observable?", ["a) 10^6", "b) 10^8", "c) 10^10", "d) 10^12"], "c"),
    Question("¿Cuál es el resultado de elevar e (la base de los logaritmos naturales) a la potencia de pi (π)?", ["a) e^e", "b) π^e", "c) ln(π)", "d) no se puede calcular"], "a"),
    Question("¿Cuál es el valor aproximado de la constante de gravitación universal (G) en unidades SI?", ["a) 6.67 x 10^-11 N·m^2/kg^2", "b)9.81 m/s^2", "c) 3.00 x 10^8 m/s", "d) 1.38 x 10^-23 J/K"], "a")
]

if __name__ == "__main__":
    main()
