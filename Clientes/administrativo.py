import socket
import sys
import os

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectar al puerto 5000 donde está escuchando el servicio
bus_address = ('localhost', 5000)
#print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        
        os.system('cls' if os.name == 'nt' else 'clear')    
        print("=" * 40)
        print("       CLIENTE ADMINISTRATIVO ")
        print("=" * 40)
        print(' [Conectando a {} puerto {}]'.format(*bus_address))
        
        print("\n MENÚ INICIO ")
        print("-" * 30)
        print(" 0) Salir")
        print(" 1) Autenticación")
        opcion = input(" Selecciona una opción: ")
    
        if opcion == "0":
            print("\n Saliendo del administrativo...")
            break  

        elif opcion == "1":
            print("\n------- AUTENTICACIÓN -------")
            servicio = b'auten'
            mensaje = servicio
            mensaje += input(" - Correo: ").encode() + b'|'
            mensaje += input(" - Contraseña: ").encode() + b'|'
            mensaje += b'administrativo'

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
                    print("       CLIENTE ADMINISTRATIVO ")
                    print("=" * 40)
                    print(' [Conectando a {} puerto {}]'.format(*bus_address))
                    
                    print(" \n MENÚ PRINCIPAL")
                    print("-" * 28)
                    print(f" ID : {id}")
                    print(" 0) Salir")
                    print(" 1) Reporte de Medicos")
                    print(" 2) Reporte Horarios")
                    opcion2 = input(" Selecciona una opción: ")
                    
                    if opcion2 == "0":
                        print(" Saliendo del menú del administrativo...")
                        break
                    
                    elif opcion2 == "1":
                        print("\n------- Reporte Medicos -------")
                        servicio = b'repor'
                        mensaje = servicio
                        mensaje += b'medicos|'
                        while True:
                            filtro = input(" - Especialidad (Pediatria, Cardiologia, General, Dermatologa) o Todos: ").strip()
                            if filtro in ['Pediatria', 'Cardiologia', 'General', 'Dermatologa', 'Todos']:
                                mensaje += filtro.encode()
                                break
                            else:
                                print(" Opción inválida !")
                    
                    elif opcion2 == "2":
                        print("\n------- Reporte Horarios -------")
                        servicio = b'repor'
                        mensaje = servicio
                        mensaje += b'horarios|'
                        mensaje += input(" - id_usuario medico: ").encode()

                    else:
                        print(" Opción inválida.")
                        continue

                    # Enviar mensaje de reporte
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
                print("Acceso denegado.")

        else:
            print("Opción inválida.")
            continue

finally:
    print(' [Cerrando socket]')
    sock.close()
