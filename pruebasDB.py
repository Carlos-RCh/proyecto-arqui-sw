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
    # Ejecutar la consulta para obtener todos los usuarios
    cursor.execute("SELECT * FROM usuario;")
    
    # Obtener todos los registros
    usuarios = cursor.fetchall()

    # Mostrar los usuarios
    print("Usuarios registrados:")
    for usuario in usuarios:
        print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Correo: {usuario[2]}, Contraseña: {usuario[3]}, ROl: {usuario[4]}")

finally:
    cursor.close()
    conn.close()
