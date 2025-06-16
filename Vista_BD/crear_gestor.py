import psycopg2

# Conectar a la base de datos
conn = psycopg2.connect(
    dbname="consultorio",
    user="carlos",
    password="213207091",
    host="localhost",
    port="6000"
)
# Crear un cursor
cur = conn.cursor()

# Insertar un nuevo usuario con rol 'gestor'
cur.execute("""
    INSERT INTO usuario (nombre, correo, contrasena, rol)
    VALUES (%s, %s, %s, %s)
""", ('gestor', 'gestor@gmail.com', '123', 'gestor'))

# Confirmar los cambios
conn.commit()

# Cerrar el cursor y la conexión
cur.close()
conn.close()

print("Usuario 'gestor' insertado correctamente.")