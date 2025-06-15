import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        print(" Opcion :")
        opcion = input(" 0) Salir 1) Registrar Usuario, 2) Autenticación: ")
        
        if opcion == "0":
            print(" Saliendo del cliente paciente...")
            break  
        
        elif opcion == "1":
            
            servicio = b'ruser'
            mensaje = servicio
            mensaje += input(" - Nombre: ").encode() + b'|'
            mensaje += input(" - Correo: ").encode() + b'|'
            mensaje += input(" - Contraseña: ").encode() + b'|'
            mensaje += b'paciente|'

            # Validar seguro de salud
            while True:
                seguro_salud = input(" - Seguro de Salud (Fonasa/Isapre/Privado/Ninguno): ").strip()
                if seguro_salud in ['Fonasa', 'Isapre', 'Privado', 'Ninguno']:
                    mensaje += seguro_salud.encode()
                    break
                else:
                    print(" Opción inválida!")

            # Enviar mensaje de registro
            numero = str(len(mensaje)).rjust(5, '0')
            mensaje = numero.encode() + mensaje
            print('Enviando {!r}'.format(mensaje))
            sock.sendall(mensaje)

            print(" [ Esperando transacción ... ]")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)

            print(" [ Verificando respuesta del servicio ... ]")
            print(' Recibido {!r}'.format(data))
            
            # Después de registrar, vuelve a la pantalla principal
            continue

        elif opcion == "2":
            # Autenticación de Usuario
            servicio = b'auten'
            mensaje = servicio
            mensaje += input(" - Ingresa correo: ").encode() + b'|'
            mensaje += input(" - Ingresa contraseña: ").encode()

            # Enviar mensaje de autenticación
            numero = str(len(mensaje)).rjust(5, '0')
            mensaje = numero.encode() + mensaje
            print('Enviando {!r}'.format(mensaje))
            sock.sendall(mensaje)

            print(" [ Esperando transacción ... ]")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)

            print(" [ Verificando respuesta del servicio ... ]")
            print(' Recibido {!r}'.format(data))
            
            mensaje = data.decode()
            datos = mensaje.split('|')

            confirmacion = datos[1]
            if confirmacion == 'true':
                print(" - Acceso exitoso.")
                acceso_permitido = True
            else:
                print(" - Acceso denegado.")
                acceso_permitido = False
                            
            
            # Si el acceso es exitoso, permitir el acceso a las opciones 3 y 4
            if acceso_permitido:
                while True:
                    print(" --------------------------------------")
                    opcion2 = input(" 1) Agendar Cita 2) Cancelar Cita 3) Ver Horarios  4) Notificar Cita : ")

                    if opcion2 == "1":
                        print(" Ingresa:")
                        servicio = b'gcita'
                        mensaje = servicio
                        mensaje += b'crear|'
                        mensaje += input(" - id_usuario cliente: ").encode() + b'|'  
                        mensaje += input(" - id_usuario medico: ").encode() + b'|'  
                        mensaje += input(" - mes/dia ").encode() + b'|'  
                        mensaje += input(" - horario AA:BB-XX:YY ").encode()  
                    
                    elif opcion2 == "2":
                        servicio = b'gcita'
                        mensaje = servicio
                        mensaje += b'cancelar|'    
                        mensaje += input(" - id_cita : ").encode() 

                    elif opcion2 == "3":
                        print("Filtrado:")
                        servicio = b'verho'
                        mensaje = servicio
                        mensaje += input(" - Especialidad (Cardiologia/Pediatria/Dermatologa/General): ").encode() + b'|'
                        
                        
                    elif opcion2 == "4":
                        servicio = b'notif'
                        mensaje = servicio
                        mensaje += input(" - Ingresa ID de cita: ").encode() + b'|'
                        mensaje += input(" - Ingresa correo del paciente: ").encode()

                    else:
                        print(" Opción inválida !")
                        continue

                    # Enviar mensaje de agendar o notificar cita
                    numero = str(len(mensaje)).rjust(5, '0')
                    mensaje = numero.encode() + mensaje
                    print('Enviando {!r}'.format(mensaje))
                    sock.sendall(mensaje)

                    print(" [ Esperando transacción ... ]")
                    amount_received = 0
                    amount_expected = int(sock.recv(5))

                    while amount_received < amount_expected:
                        data = sock.recv(amount_expected - amount_received)
                        amount_received += len(data)

                    print(" [ Verificando respuesta del servicio ... ]")
                    print('Recibido {!r}'.format(data))

                    # Salir del ciclo si el usuario decide no continuar
                    continuar = input("¿Deseas continuar con otra opción? (y/n): ")
                    if continuar.lower() != 'y':
                        break

            # Si no tiene acceso, volver al menú principal
            else:
                print(" Acceso denegado.")

        else:
            print(" Opción inválida !")
            continue

finally:
    print('Cerrando socket')
    sock.close()
