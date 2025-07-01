import socket
import sys
import psycopg2

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al puerto 5000 donde está escuchando el servicio
bus_address = ('localhost', 5000)
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
    sock.sendall(message)
    sinit = 1

    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)

        print("=" * 40)
        print("       SERVICIO AGENDA MEDICA ")
        print('\n Respuesta : [{!r}]'.format(data))

        
        if sinit == 1:
            sinit = 0
            print(" Mensaje (sinit answer): servicio OK")
        else:
            mensaje = data.decode()
            servicio = mensaje[:5]  # 'agmed'
            datos = mensaje[5:].split('|')

            id_usuario = datos[0]
            fecha = datos[1]
            hora = datos[2]

            # Verificar si el usuario existe y obtener el rol
            cursor.execute("SELECT rol FROM usuario WHERE id = %s", (id_usuario,))
            resultado = cursor.fetchone()

            if resultado:
                rol = resultado[0]

                if rol == 'medico':
                    cursor.execute("SELECT id FROM medico WHERE id_usuario = %s", (id_usuario,))
                    medico = cursor.fetchone()

                    if medico:
                        id_medico = medico[0]
                        cursor.execute("""
                            SELECT COUNT(*) FROM horario 
                            WHERE id_medico = %s AND fecha = %s AND horario = %s
                        """, (id_medico, fecha, hora))

                        horario_existente = cursor.fetchone()[0]

                        if horario_existente == 0:
                            cursor.execute("""
                                INSERT INTO horario (id_medico, fecha, horario, disponible)
                                VALUES (%s, %s, %s, TRUE)
                            """, (id_medico, fecha, hora))

                            conn.commit()
                            respuesta = b'00020agmedRegistroExitoso'
                            print(' Enviando  : [{!r}]'.format(respuesta))    
                            sock.sendall(respuesta)
                        else:
                            respuesta = b'00021agmedHorarioExistente'
                            print(' Enviando  : [{!r}]'.format(respuesta))    
                            sock.sendall(respuesta)
                    else:
                        respuesta = b'00018agmedRegistroFallo'
                        print(' Enviando  : [{!r}]'.format(respuesta))    
                        sock.sendall(respuesta)

                elif rol == 'paciente':
                        # 1. Obtener todos los id_usuario con rol 'medico'
                        cursor.execute("SELECT id FROM usuario WHERE rol = 'medico'")
                        usuarios_medicos = cursor.fetchall()

                        horarios_info = []

                        for usuario_medico in usuarios_medicos:
                            id_usuario_medico = usuario_medico[0]

                            # 2. Obtener id de la tabla medico usando id_usuario
                            especialidad = fecha
                            cursor.execute("SELECT id FROM medico WHERE id_usuario = %s AND especialidad = %s", (id_usuario_medico, especialidad))
                            medico = cursor.fetchone()
                            if medico:
                                id_medico = medico[0]

                                # 3. Obtener horarios del médico (fecha y horario)
                                cursor.execute("""
                                    SELECT id, fecha, horario FROM horario
                                    WHERE id_medico = %s
                                """, (id_medico,))
                                horarios = cursor.fetchall()

                                for id_horario, fecha, hora in horarios:
                                    horarios_info.append(f"{id_usuario_medico}-{id_horario}-{fecha}-{hora}")

                        # 4. Crear respuesta como string concatenado
                        mensaje_respuesta = "true|" + "|".join(horarios_info)
                        longitud = str(len(mensaje_respuesta) + 5).rjust(5, '0')
                        respuesta = longitud.encode() + b'agmed' + mensaje_respuesta.encode()
                        print(' Enviando  : [{!r}]'.format(respuesta))    
                        sock.sendall(respuesta)
                    
                else:
                    respuesta = b'00016agmedRolInvalido'
                    print(' Enviando  : [{!r}]'.format(respuesta))    
                    sock.sendall(respuesta)
            else:
                respuesta = b'00020agmedUsuarioNoExiste'        
                print(' Enviando  : [{!r}]'.format(respuesta))    
                sock.sendall(respuesta)
        
            
        print("=" * 40)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
