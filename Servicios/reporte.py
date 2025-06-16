import socket
import sys
import psycopg2

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al puerto 5000 donde está escuchando el servicio
bus_address = ('localhost', 5000)
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
    # Enviar mensaje de inicio para iniciar el servicio de reporte
    message = b'00010sinitrepor'
    print('Enviando {!r}'.format(message))
    sock.sendall(message)
    sinit = 1

    while True:
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
            servicio = mensaje[:5]  # 'repor'
            datos = mensaje[5:].split('|')

            
            filtro = datos[1]  # El filtro que se pasó (ej: 'Pediatria', 'Todos', etc.)

            print(f"Filtro recibido: {filtro}")

            if filtro == 'Todos':  # Si el filtro es 'Todos', obtener todos los médicos
                cursor.execute("SELECT id_usuario, especialidad FROM medico")
                medicos = cursor.fetchall()

                # Preparar la respuesta
                respuesta = b'repor|'
                for medico in medicos:
                    id_usuario, especialidad = medico
                    respuesta += f"{id_usuario},{especialidad}|".encode()

            else:  # Si el filtro es alguna especialidad específica
                cursor.execute("""
                    SELECT id_usuario, especialidad FROM medico
                    WHERE especialidad = %s
                """, (filtro,))
                medicos = cursor.fetchall()

                # Preparar la respuesta
                respuesta = b'repor|'
                for medico in medicos:
                    id_usuario, especialidad = medico
                    respuesta += f"{id_usuario},{especialidad}|".encode()
            

            # Enviar la respuesta al cliente
            numero = str(len(respuesta)).rjust(5, '0')
            respuesta = numero.encode() + respuesta
            print('Enviando {!r}'.format(respuesta))
            sock.sendall(respuesta)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
