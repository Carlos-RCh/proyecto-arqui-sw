import socket
import sys
import psycopg2

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

# Connect to the database
conn = psycopg2.connect(
    dbname="consultorio",
    user="carlos",
    password="213207091",
    host="localhost",
    port="6000"
)
cursor = conn.cursor()

try:
    # Send initial message to start the service
    message = b'00010sinitguser'
    print('Enviando {!r}'.format(message))
    sock.sendall(message)
    sinit = 1

    while True:
        # Waiting for transaction
        print(" [ Esperando transacción ... ]")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)

        print(" [ Procesando ... ]")
        print(' -Mensaje recibido {!r}'.format(data))

        if sinit == 1:
            sinit = 0
            print(' -Recibido mensaje de inicio (sinit answer)')
        else:
            mensaje = data.decode()
            servicio = mensaje[:5]  # 'guser'
            datos = mensaje[5:].split('|')

            accion = datos[0]  # 'eliminar'
            id_usuario = datos[1]

            print(f"Acción: {accion}, ID Usuario: {id_usuario}")

            if accion == 'eliminar':
                # Verificar si el usuario existe
                cursor.execute("SELECT COUNT(*) FROM usuario WHERE id = %s", (id_usuario,))
                usuario_existente = cursor.fetchone()[0]

                if usuario_existente > 0:  # El usuario existe
                    # Eliminar el usuario de la tabla usuario
                    cursor.execute("DELETE FROM usuario WHERE id = %s", (id_usuario,))

                    conn.commit()
                    respuesta = b'00014guserUsuarioEliminado'
                    sock.sendall(respuesta)
                else:
                   
                    respuesta = b'00015guserUsuarioNoEncontrado'
                    sock.sendall(respuesta)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
