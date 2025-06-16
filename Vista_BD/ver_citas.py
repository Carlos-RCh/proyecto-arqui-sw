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

# Obtener todas las citas con el id, id_horario y estado
cursor.execute("""
    SELECT c.id, c.id_horario, c.estado
    FROM cita c
""")
citas = cursor.fetchall()

# Mostrar las citas
for cita in citas:
    id_cita, id_horario, estado = cita
    print(f"ID Cita: {id_cita}, ID Horario: {id_horario}, Estado: {estado}")
    print("")

# Cerrar la conexión
cursor.close()
conn.close()
