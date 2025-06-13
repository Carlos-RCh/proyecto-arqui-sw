import psycopg2

# Conectar a la base de datos
conn = psycopg2.connect(
    dbname="consultorio",  # Nombre de tu base de datos
    user="carlos",         # Tu usuario de la base de datos
    password="213207091",  # Tu contraseña de la base de datos
    host="localhost",      # Dirección del servidor de base de datos
    port="6000"            # Puerto de conexión
)

cursor = conn.cursor()

# Ejecutar consulta para obtener todas las tablas en el esquema público
cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
""")

# Obtener todas las tablas
tablas = cursor.fetchall()

# Mostrar todas las tablas
print("Tablas en la base de datos:")
for tabla in tablas:
    print(tabla[0])

# Cerrar la conexión
cursor.close()
conn.close()
