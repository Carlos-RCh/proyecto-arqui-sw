# message = b'00010sinitauten'
# message = b'00013autenReceived'


import socket
import sys
import psycopg2

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)  # Dirección del bus SOA
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

# Conectar a la base de datos
conn = psycopg2.connect(
    dbname="consultorio",
    user="carlos",
    password="213207091",
    host="localhost",
    port="6000"
)
cursor = conn.cursor()


try:
    # Enviar mensaje de inicio
    message = b'00010sinitauten'
    print('Enviando {!r}'.format(message))
    sock.sendall(message)
    
    sinit = 1

    while True:
        print(" [ Esperando transacción ... ]")
        amount_expected = int(sock.recv(5))
        data = b""
        while len(data) < amount_expected:
            data += sock.recv(amount_expected - len(data))

        print(" [ Procesando ... ]")
        print(' -Mensaje recibido {!r}'.format(data))

        if sinit == 1:
            sinit = 0
            print(' -Recibido mensaje de inicio (sinit answer)')
        else:
            mensaje = data.decode()
            servicio = mensaje[:5]
            datos = mensaje[5:].split('|')

            correo = datos[0]
            contrasena = datos[1]

            print(f" [ Servicio: {servicio}, Correo: {correo}, Contraseña: {contrasena} ]")

            # Verificar si el usuario existe
            cursor.execute("""
                SELECT * FROM usuario WHERE correo = %s AND contrasena = %s
            """, (correo, contrasena))

            # Si el correo y la contraseña coinciden, obtiene un registro
            usuario = cursor.fetchone()  

            if usuario:
                print(" -Acceso exitoso.")
                respuesta = b'00033autenReceived|true|Acceso Exitoso'
            else:
                print(" -Acceso denegado.")
                respuesta = b'00035autenReceived|false|Acceso Denegado'

            sock.sendall(respuesta)  # Enviar la respuesta al cliente
finally:
    print(' Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
