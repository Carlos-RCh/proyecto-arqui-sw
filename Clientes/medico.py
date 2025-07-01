import socket
import sys
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)
#print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')    
        print("=" * 40)
        print("       CLIENTE MÉDICO ")
        print("=" * 40)
        print(' [Conectando a {} puerto {}]'.format(*bus_address))
        
        print("\n MENÚ INICIO ")
        print("-" * 30)
        print(" 0) Salir")
        print(" 1) Autenticación")
        opcion = input(" Selecciona una opción: ")

        if opcion == "0":
            print("\n Saliendo del medico...")
            break  
        
        elif opcion == "1":
            print("\n------- AUTENTICACIÓN -------")
            servicio = b'auten'
            mensaje = servicio
            mensaje += input(" - Correo: ").encode() + b'|'
            mensaje += input(" - Contraseña: ").encode() + b'|'
            mensaje += b'medico'
        
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
                    print("       CLIENTE MÉDICO ")
                    print("=" * 40)
                    print(' [Conectando a {} puerto {}]'.format(*bus_address))
                    
                    print(" \n MENÚ PRINCIPAL")
                    print(f" ID : {id}")
                    print("-" * 28)
                    print(" 0) Salir")
                    print(" 1) Agenda Medica")
                    print(" 2) Ver Historia Clinica")
                    print(" 3) Crear Historia Clinica")
                    opcion2 = input(" Selecciona una opción: ")
            
                    if opcion2 == "0":
                        print(" Saliendo del menú del médico...")
                        break
                    
                    elif opcion2 == "1":
                       print("\n------- Agenda Medica -------")
                       servicio = b'agmed'
                       mensaje = servicio
                       mensaje += input(" - id_usuario medico: ").encode() + b'|'  
                       mensaje += input(" - día/mes ").encode() + b'|'  
                       mensaje += input(" - horario 'AA:BB' : ").encode()  
                       
                    elif opcion2 == "2":
                        print("\n------- Historia Clinica -------")
                        servicio = b'hclin' 
                        mensaje = servicio
                        mensaje +=  b'ver|' 
                        mensaje += input(" - id_usuario de paciente: ").encode()
                        
                    elif opcion2 == "3":    
                        print("\n------- Crea Historia -------")
                        servicio = b'hclin' 
                        mensaje = servicio
                        mensaje +=  b'crear|' 
                        mensaje += input(" - id_usuario de paciente: ").encode() + b'|'
                        mensaje += input(" - Diagnostico : ").encode() + b'|'
                        mensaje += input(" - Tratamiento : ").encode() 
                        
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
