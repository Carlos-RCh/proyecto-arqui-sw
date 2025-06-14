import socket
import sys

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:

        opcion = input("Opción 1) Autenticación: ")    
        
        if opcion == "1":
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

            if acceso_permitido:
                while True:
                    opcion2 = input(" Opción 1) Gestionar Medico, 2) Gestionar Admin: ")
                    
                    if opcion2 == "1":  # Gestión Médicos
                        
                        accion = input(" ¿Deseas crear o eliminar médico? (crear/eliminar): ").strip().lower()

                        if accion == "eliminar":
                            servicio = b'guser'
                            mensaje = servicio
                            mensaje += b"eliminar|"
                            id_medico = input(" - Ingresa ID del médico a eliminar: ").encode()
                            mensaje += id_medico
                            
                        elif accion == "crear":
                            servicio = b'ruser'
                            mensaje = servicio
                            mensaje += input(" - Nombre: ").encode() + b'|'
                            mensaje += input(" - Correo: ").encode() + b'|'
                            mensaje += input(" - Contraseña: ").encode() + b'|'
                            mensaje += b'medico|'
            
                            while True:
                                especialidad = input(" - Especialidad (Cardiologia/Pediatria/Dermatologa/General): ").strip()
                                if especialidad in ['Pediatria', 'Cardiologia', 'General', 'Dermatologa']:
                                    mensaje += especialidad.encode()
                                    break
                                else:
                                    print(" Opción inválida !")
                            
                        else:
                            print("Opción inválida. Intenta nuevamente.")
                            continue
                        
                    elif opcion2 == "2":  # Gestión Admin
                        
                        accion = input("¿Deseas crear o eliminar administrador? (crear/eliminar): ").strip().lower()
            
                        if accion == "eliminar":
                            servicio = b'guser'
                            mensaje = servicio
                            mensaje += b"eliminar|"
                            id_admin = input("Ingresa ID del administrador a eliminar: ").encode() + b'|'
                            mensaje += id_admin
                        
                        elif accion == "crear":
                            servicio = b'ruser'
                            mensaje = servicio
                            mensaje += input(" - Nombre: ").encode() + b'|'
                            mensaje += input(" - Correo: ").encode() + b'|'
                            mensaje += input(" - Contraseña: ").encode() + b'|'
                            mensaje += b'administrativo|'
                            mensaje += b'extra'
                            
                        else:
                            print("Opción inválida. Intenta nuevamente.")
                            continue
                        
                    else:
                        print("Opción inválida.")
                        continue
                    
                    # Agregar longitud del mensaje
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
                  
            else:
                print(" Acceso denegado.")
        
        else:
            print(" Opción inválida !")
            continue
        
finally:
    print('closing socket')
    sock.close()
