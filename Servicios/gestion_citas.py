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
    # Enviar mensaje de inicio para iniciar el servicio de gestión de citas
    message = b'00010sinitgcita'
    # print('Enviando {!r}'.format(message))
    sock.sendall(message)
    
    sinit = 1

    while True:
        
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)

        print("=" * 40)
        print("       SERVICIO GESTION CITAS ")
        
        print(' \n Respuesta : [{!r}]'.format(data))
    

        if sinit == 1:
            sinit = 0
            print(" Mensaje (sinit answer): servicio OK")
        else:
            mensaje = data.decode()
            servicio = mensaje[:5]  # 'gcita'
            datos = mensaje[5:].split('|')
            # Guardar si crear o cancelar cita
            accion = datos[0] 
    
            if accion == 'cancelar': # Cancelar cita
                id_cita = datos[1]

                # Buscar la cita con el id_cita y obtener el id_horario asociado
                cursor.execute("SELECT id_horario FROM cita WHERE id = %s", (id_cita,))
                resultado_cita = cursor.fetchone()

                if resultado_cita:
                    id_horario = resultado_cita[0]
                    
                    # Actualizar el estado de la cita a 'cancelada'
                    cursor.execute("""
                    UPDATE cita
                    SET estado = 'cancelada'
                    WHERE id = %s
                    """, (id_cita,))

                    # Actualizar el estado de disponible a TRUE en la tabla horario
                    cursor.execute("""
                    UPDATE horario
                    SET disponible = TRUE
                    WHERE id = %s
                    """, (id_horario,))

                    conn.commit()  # Guardar cambios en la base de datos
                    respuesta = b'00014gcitaCancelada'
                    print(' Enviando  : [{!r}]'.format(respuesta))
                    sock.sendall(respuesta)
                else:
                    respuesta = b'00015gcitaErrorCancelacion'
                    print(' Enviando  : [{!r}]'.format(respuesta))
                    sock.sendall(respuesta)
                continue
            
            
            elif accion == 'ver':
                id_usuario_paciente = datos[1]

                # Obtener id del paciente a partir del id_usuario
                cursor.execute("SELECT id FROM paciente WHERE id_usuario = %s", (id_usuario_paciente,))
                paciente = cursor.fetchone()

                if paciente:
                    id_paciente = paciente[0]
                    # Obtener todas las citas del paciente, junto con fecha y hora del horario asociado
                    cursor.execute("""
                    SELECT c.id, h.fecha, h.horario
                    FROM cita c
                    JOIN horario h ON c.id_horario = h.id
                    WHERE c.id_paciente = %s
                    """, (id_paciente,))

                    citas = cursor.fetchall()

                    if citas:
                        detalles = [f"{id_cita}-{fecha}-{hora}" for id_cita, fecha, hora in citas]
                        mensaje = "true|" + "|".join(detalles)
                    else:
                        mensaje = "true|"

                    # Preparar y enviar respuesta
                    longitud = str(len(mensaje)).rjust(5, '0')
                    respuesta = longitud.encode() + b'gcita' + mensaje.encode()
                    print(" Enviando :", respuesta)
                    sock.sendall(respuesta)
                else:
                    respuesta = b'00021gcitaPacienteNoExiste'
                    print(' Enviando  : [{!r}]'.format(respuesta))
                    sock.sendall(respuesta)
                continue


            # Crear Citas y  Extraer los datos
            id_usuario_paciente = datos[1]
            id_usuario_medico = datos[2]
            fecha = datos[3]
            horario = datos[4]            
            
            print(f"Recibido - ID Usuario Cliente : {id_usuario_paciente}, ID Usuario Médico: {id_usuario_medico}, Fecha: {fecha}, Hora: {horario}")

            # Verificar si el médico existe y obtener su id_medico
            cursor.execute("SELECT id FROM medico WHERE id_usuario = %s", (id_usuario_medico,))
            medico = cursor.fetchone()
            
            if medico:  # Si el médico existe
                id_medico = medico[0]  # Obtenemos el id del médico
                
                # Verificar si el paciente existe y obtener su id_paciente
                cursor.execute("SELECT id FROM paciente WHERE id_usuario = %s", (id_usuario_paciente,))
                paciente = cursor.fetchone()
                
                if paciente:  # Si el paciente existe
                    id_paciente = paciente[0]
                    
                    # Verificar si existe el horario en la tabla horario y si está disponible
                    cursor.execute("""
                    SELECT id, disponible FROM horario 
                    WHERE id_medico = %s AND fecha = %s AND horario = %s
                    """, (id_medico, fecha, horario))
                    horario_resultado = cursor.fetchone()

                    if horario_resultado:  # Si el horario existe
                        id_horario, disponible = horario_resultado

                        if disponible:  # Si está disponible
                            # Crear la cita en la tabla cita
                            estado = 'confirmada'
                            cursor.execute("""
                            INSERT INTO cita (id_horario, estado, id_paciente, id_medico)
                            VALUES (%s, %s, %s ,%s)
                            """, (id_horario, estado, id_paciente, id_medico))
                            
                            cursor.execute("SELECT id FROM cita WHERE id_horario = %s AND id_paciente = %s AND id_medico = %s", (id_horario, id_paciente, id_medico))
                            cita = cursor.fetchone()  # Obtenemos la cita recién creada
                            
                            # Actualizar el estado de disponible a FALSE en la tabla horario
                            cursor.execute("""
                            UPDATE horario
                            SET disponible = FALSE
                            WHERE id = %s
                            """, (id_horario,))

                            conn.commit()
                            
                            respuesta = b'gcitaExitoso|'
                            respuesta += str(cita[0]).encode()        
                            numero = str(len(respuesta)).rjust(5, '0')
                            respuesta = numero.encode() + respuesta
                            print(' Enviando  : [{!r}]'.format(respuesta))
                            sock.sendall(respuesta)
                        else:
                            respuesta = b'00024gcitaHorarioNoDisponible'
                            print(' Enviando  : [{!r}]'.format(respuesta))
                            sock.sendall(respuesta)
                    else:
                        respuesta = b'00020gcitaHorarioNoExiste'
                        print(' Enviando  : [{!r}]'.format(respuesta))
                        sock.sendall(respuesta)
                else:
                    respuesta = b'00010gcitaFallo'
                    print(' Enviando  : [{!r}]'.format(respuesta))
                    sock.sendall(respuesta)
            
            else:
                respuesta = b'00010gcitaFallo'
                print(' Enviando  : [{!r}]'.format(respuesta))
                sock.sendall(respuesta)
        
        print("=" * 40)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
