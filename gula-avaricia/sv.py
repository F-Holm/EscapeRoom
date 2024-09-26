import socket
from enum import Enum

#from enum import Enum
class Codigos(Enum):
    START = b'\x00' # Inicia el juego
    RESTART = b'\x01' # Reinicia el juego
    STOP = b'\x02' # Detiene el juego pero puede volver a iniciarse
    CLOSE = b'\x03' # Detiene el juego y no puede volver a iniciarse
    TERMINO = b'\x04' # Indica que el juego terminó. Esto se manda desde el juego al sistema

# Crear un socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtener la IP privada de la computadora
#hostname = socket.gethostname()
#ip_privada = socket.gethostbyname(hostname)
ip_privada = "192.168.123.1"

# Enlazar el socket a la dirección y puerto
#servidor.bind((ip_privada, 8080))

servidor.connect((ip_privada, 8080))

# Mostrar la IP privada y el puerto
print(f"Servidor iniciado en IP: {ip_privada}, Puerto: 8080")

# Escuchar conexiones entrantes
#servidor.listen(1)
print("Esperando conexiones...")
servidor.setblocking(False)

# Aceptar una conexión
#conexion, direccion = servidor.accept()
#print(f"Conectado a {direccion}")

# Recibir datos
while True:
    #datos = servidor.recv(1024)
    num = int(input("1. START\n2. RESTART\n3. STOP\n4. CLOSE\n5. EXIT\n6. CONTINUE\n"))
    if (num == 1):
        servidor.sendall(Codigos.START.value)
    elif (num == 2):
        servidor.sendall(Codigos.RESTART.value)
    elif (num == 3):
        servidor.sendall(Codigos.STOP.value)
        print("Deteniendo el juego...")
    elif (num == 4):
        servidor.sendall(Codigos.CLOSE.value)
    elif (num == 5):
        break
    elif (num == 6):
        continue

# Cerrar la conexión
servidor.close()