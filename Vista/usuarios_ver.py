import psycopg2

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
    # Consultar todos los usuarios en la tabla 'usuario'
    cursor.execute("SELECT id, nombre, correo, rol FROM usuario")
    
    # Obtener todos los resultados
    usuarios = cursor.fetchall()

    # Mostrar todos los usuarios
    for usuario in usuarios:
        print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Correo: {usuario[2]}, Rol: {usuario[3]}")

finally:
    # Cerrar la conexión
    cursor.close()
    conn.close()
