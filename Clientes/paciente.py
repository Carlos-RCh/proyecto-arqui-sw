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
        print("       CLIENTE PACIENTE ")
        print("=" * 40)
        print(' [Conectando a {} puerto {}]'.format(*bus_address))
        
        print("\n MENÚ INICIO ")
        print("-" * 30)
        print(" 0) Salir")
        print(" 1) Registrar Paciente")
        print(" 2) Autenticación")
        opcion = input(" Selecciona una opción: ")
        
        if opcion == "0":
            print("\n Saliendo del paciente...")
            break  
        
        elif opcion == "1":
            print("\n--------- REGISTRO ---------")
            servicio = b'ruser'
            mensaje = servicio
            mensaje += input(" - Nombre: ").encode() + b'|'
            mensaje += input(" - Correo: ").encode() + b'|'
            mensaje += input(" - Contraseña: ").encode() + b'|'
            mensaje += b'paciente|'

            while True:
                seguro_salud = input(" - Seguro de Salud (Fonasa/Isapre/Privado/Ninguno): ").strip()
                if seguro_salud in ['Fonasa', 'Isapre', 'Privado', 'Ninguno']:
                    mensaje += seguro_salud.encode()
                    break
                else:
                    print(" Opción inválida!")
            
            
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
            continue

        elif opcion == "2":
            print("\n------- AUTENTICACIÓN -------")
            servicio = b'auten'
            mensaje = servicio
            mensaje += input(" - Correo: ").encode() + b'|'
            mensaje += input(" - Contraseña: ").encode() + b'|'
            mensaje += b'paciente'

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
                    print("       CLIENTE PACIENTE ")
                    print("=" * 40)
                    print(' [Conectando a {} puerto {}]'.format(*bus_address))
                    
                    print(" \n MENÚ PRINCIPAL ")
                    print(f" ID : {id}")
                    print("-" * 28)
                    print(" 0) Salir")
                    print(" 1) Agendar Cita")
                    print(" 2) Cancelar Cita")
                    print(" 3) Ver Citas")
                    print(" 4) Ver Horiarios")
                    print(" 5) Notificar Cita")
                    
                    
                    opcion2 = input(" Selecciona una opción: ")

                    if opcion2 == "0":
                        print(" Saliendo del menú del paciente...")
                        break

                    elif opcion2 == "1":
                        print("\n------- Agendar Cita -------")
                        servicio = b'gcita'
                        mensaje = servicio
                        mensaje += b'crear|'
                        mensaje += input(" - id_usuario cliente: ").encode() + b'|'  
                        mensaje += input(" - id_usuario medico: ").encode() + b'|'  
                        mensaje += input(" - dia/mes: ").encode() + b'|'  
                        mensaje += input(" - horario 'AA:BB' : ").encode()  

                    elif opcion2 == "2":
                        print("\n------- Cancelar Cita -------")
                        servicio = b'gcita'
                        mensaje = servicio
                        mensaje += b'cancelar|'    
                        mensaje += input(" - id_cita: ").encode() 
                    
                    elif opcion2 == "3":
                        print("\n------- Ver Citas -------")
                        servicio = b'gcita'
                        mensaje = servicio
                        mensaje += b'ver|'    
                        mensaje += input(" - id_usuario cliente: ").encode() + b'|'  
                    
                    elif opcion2 == "4":
                        print("\n------- Ver Horarios -------")
                        servicio = b'agmed'
                        mensaje = servicio
                        mensaje += input(" - id_usuario paciente: ").encode() + b'|'
                        while True:
                                especialidad = input(" - Especialidad (Cardiologia/Pediatria/Dermatologia/General): ").strip()
                                if especialidad in ['Pediatria', 'Cardiologia', 'General', 'Dermatologia']:
                                    mensaje += especialidad.encode()
                                    break
                                else:
                                    print(" Opción inválida !")
                                        
                        mensaje += b'|x'  
                        
                    elif opcion2 == "5":
                        print("\n------- Notificar Cita -------")
                        servicio = b'notif'
                        mensaje = servicio
                        mensaje += input(" - Ingresa id_usuario paciente: ").encode() + b'|'
                        mensaje += input(" - Ingresa id_cita: ").encode()

                    else:
                        print(" Opción inválida !")
                        continue

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
    print(" [Cerrando socket...]")
    sock.close()
