import socket

# Crear un socket TCP/IP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
ip_servidor = input("Ingrese la dirección IP del servidor: ")
cliente.connect((ip_servidor, 8080))

# Enviar datos
while True:
    mensaje = int(input("Ingrese un mensaje: "))
    if (mensaje == ""): continue
    cliente.sendall(chr(mensaje).encode())
    if mensaje == chr(0):
        break

# Cerrar la conexión
cliente.close()

