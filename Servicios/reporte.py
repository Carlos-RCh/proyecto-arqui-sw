import socket
import sys
import psycopg2

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al puerto 5000 donde está escuchando el servicio
bus_address = ('localhost', 5000)
# print('Conectando a {} puerto {}'.format(*bus_address))
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
    #print('Enviando {!r}'.format(message))
    sock.sendall(message)
    sinit = 1

    while True:
        # print(" [ Esperando transacción ... ]")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)

        print("=" * 40)
        print("       SERVICIO REPORTE ")
        
        print(' \n Respuesta : [{!r}]'.format(data))

        if sinit == 1:
            sinit = 0
            print(' Mnesjae (sinit answer): servicio OK')
        else:
            mensaje = data.decode()
            servicio = mensaje[:5]  # 'repor'
            datos = mensaje[5:].split('|')

            tipo_reporte = datos[0]  # 'medicos' o 'horarios'
            filtro = datos[1]     

            if tipo_reporte == 'medicos':
                if filtro == 'Todos':
                    cursor.execute("SELECT id_usuario, especialidad FROM medico")
                    medicos = cursor.fetchall()
                else:
                    cursor.execute("SELECT id_usuario, especialidad FROM medico WHERE especialidad = %s", (filtro,))
                    medicos = cursor.fetchall()

                respuesta = b'repor|'
                for medico in medicos:
                    id_usuario, especialidad = medico
                    respuesta += f"{id_usuario},{especialidad}|".encode()

            elif tipo_reporte == 'horarios':
                id_usuario_medico = filtro

                # Obtener id del médico desde la tabla medico
                cursor.execute("SELECT id FROM medico WHERE id_usuario = %s", (id_usuario_medico,))
                medico = cursor.fetchone()

                if medico:
                    id_medico = medico[0]

                    # Obtener todos los horarios de ese médico
                    cursor.execute("""
                        SELECT id, fecha, horario FROM horario
                        WHERE id_medico = %s
                    """, (id_medico,))
                    horarios = cursor.fetchall()

                    # Armar la respuesta
                    respuesta = b'repor|'
                    for id_horario, fecha, hora in horarios:
                        respuesta += f"{id_horario}-{fecha}-{hora}|".encode()
                else:
                    respuesta = b'repor|MedicoNoEncontrado|'
    
            # Enviar respuesta
            numero = str(len(respuesta)).rjust(5, '0')
            respuesta = numero.encode() + respuesta
            print(' Respuesta : [{!r}]'.format(respuesta))
            sock.sendall(respuesta)

        print("=" * 40)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
