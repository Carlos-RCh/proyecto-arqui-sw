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
    # Enviar mensaje de inicio
    message = b'00010sinitagmed'
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
            servicio = mensaje[:5]  # 'agmed'
            datos = mensaje[5:].split('|')
            
            # Extraer los datos
            id_usuario = datos[0]
            fecha = datos[1]
            hora = datos[2]

            print(f" Recibido - ID Usuario: {id_usuario}, Fecha: {fecha}, Hora: {hora}")

            # Verificar si el médico existe
            cursor.execute("SELECT id FROM medico WHERE id_usuario = %s", (id_usuario,))
            medico = cursor.fetchone()
            
            if medico:  # Si el médico existe
                id_medico = medico[0]  # Aquí estamos obteniendo el id del médico 
                # Verificar si ya existe un horario para ese médico con la misma fecha y hora
                cursor.execute("""
                SELECT COUNT(*) FROM horario 
                WHERE id_medico = %s AND fecha = %s AND horario = %s
                """, (id_medico, fecha, hora))

                horario_existente = cursor.fetchone()[0]

                if horario_existente == 0:  # Si no existe, insertamos el nuevo horario
                    
                    cursor.execute("""
                    INSERT INTO horario (id_medico, fecha, horario, disponible)
                    VALUES (%s, %s, %s, TRUE)
                    """, (id_medico, fecha, hora))

                    conn.commit()
                    print(" - Nuevo horario creado para el médico.")
                    # Enviar respuesta de éxito
                    respuesta = b'00020agmedRegistroExitoso'
                    sock.sendall(respuesta)
                else:
                    print(" - El horario ya existe para el médico en esa fecha y hora.")
                    respuesta = b'00021agmedHorarioExistente'
                    sock.sendall(respuesta)

            else:
                # Si el médico no existe, enviar mensaje de fallo
                print(" - El médico no existe.")
                respuesta = b'00018agmedRegistroFallo'
                sock.sendall(respuesta)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
