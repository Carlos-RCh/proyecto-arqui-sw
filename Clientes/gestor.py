import socket
import sys
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5500)
sock.connect(bus_address)

try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print("       CLIENTE GESTOR ")
        print("=" * 40)
        print(' [Conectando a {} puerto {}]'.format(*bus_address))
        
        print("\n MENÚ INICIO ")
        print("-" * 30)
        print(" 0) Salir")
        print(" 1) Autenticación")
        opcion = input(" Selecciona una opción: ")
        
        if opcion == "0":
            print("\n Saliendo del gestor...")
            break  
        
        elif opcion == "1":
            # Autenticación de Usuario
            print("\n------- AUTENTICACIÓN -------")
            servicio = b'auten'
            mensaje = servicio
            mensaje += input(" - Correo: ").encode() + b'|'
            mensaje += input(" - Contraseña: ").encode() + b'|'
            mensaje += b'gestor'

            # Enviar mensaje de autenticación
            numero = str(len(mensaje)).rjust(5, '0')
            mensaje = numero.encode() + mensaje
            print('\n Enviando  : [{!r}]'.format(mensaje))
            sock.sendall(mensaje)
            #print(" [ Esperando transacción ... ]")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)

            print(' Respuesta : [{!r}]'.format(data))
            
            mensaje = data.decode()
            datos = mensaje.split('|')

            confirmacion = datos[1]
            id = datos[2]
            
            if confirmacion == 'true':                
                acceso_permitido = True
            else:                
                acceso_permitido = False

            if acceso_permitido:
                os.system('cls' if os.name == 'nt' else 'clear')    
                while True:
                    print("=" * 40)
                    print("       CLIENTE GESTOR ")
                    print("=" * 40)
                    print(' [Conectando a {} puerto {}]'.format(*bus_address))
                    
                    print(" \n MENÚ PRINCIPAL")
                    print("-" * 28)
                    print(f" ID : {id}")
                    print(" 0) Salir")
                    print(" 1) Gestionar Medico")
                    print(" 2) Gestionar Admin:")
                    opcion2 = input(" Selecciona una opción: ")
                    
                    if opcion2 == "0":
                        print(" Saliendo del menú del gestor...")
                        break
                    
                    if opcion2 == "1":  # Gestión Médicos
                        
                        print("\n------- GESTIONAR MEDICO -------")
                        accion = input(" ¿Deseas (crear/eliminar) médico? : ").strip().lower()

                        if accion == "eliminar":
                            print(" Ingresar :")
                            servicio = b'guser'
                            mensaje = servicio
                            mensaje += b"eliminar|"
                            id_medico = input(" - id_usuario médico a eliminar: ").encode()
                            mensaje += id_medico
                            
                        elif accion == "crear":
                            servicio = b'ruser'
                            mensaje = servicio
                            mensaje += input(" - Nombre: ").encode() + b'|'
                            mensaje += input(" - Correo: ").encode() + b'|'
                            mensaje += input(" - Contraseña: ").encode() + b'|'
                            mensaje += b'medico|'
            
                            while True:
                                especialidad = input(" - Especialidad (Cardiologia/Pediatria/Dermatologia/General): ").strip()
                                if especialidad in ['Pediatria', 'Cardiologia', 'General', 'Dermatologa']:
                                    mensaje += especialidad.encode()
                                    break
                                else:
                                    print(" Opción inválida !")
                            
                        else:
                            print("Opción inválida.")
                            continue
                        
                    elif opcion2 == "2":  # Gestión Admin
                        print("\n------- GESTIONAR ADMINISTRADOR -------")
                        accion = input("¿Deseas (crear/eliminar) administrador? : ").strip().lower()
            
                        if accion == "eliminar":
                            print(" Ingresar :")
                            servicio = b'guser'
                            mensaje = servicio
                            mensaje += b"eliminar|"
                            id_admin = input(" - id_usuario admin a eliminar: ").encode() + b'|'
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
                            print("Opción inválida.")
                            continue
                        
                    else:
                        print("Opción inválida.")
                        continue
                    
                    # Agregar longitud del mensaje
                    numero = str(len(mensaje)).rjust(5, '0')
                    mensaje = numero.encode() + mensaje
                    print('\n Enviando  : [{!r}]'.format(mensaje))
                    sock.sendall(mensaje)
            
                    amount_received = 0
                    amount_expected = int(sock.recv(5))
            
                    while amount_received < amount_expected:
                        data = sock.recv(amount_expected - amount_received)
                        amount_received += len(data)
                        
                    print(' Respuesta : [{!r}]'.format(data))
                
        else:
            print(" Opción inválida !")
            continue
        
finally:
    print('closing socket')
    sock.close()
