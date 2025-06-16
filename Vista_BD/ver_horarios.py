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

# Obtener todos los horarios
cursor.execute("""
    SELECT id, fecha, horario, disponible
    FROM horario
""")
horarios = cursor.fetchall()

# Mostrar los resultados
for horario in horarios:
    id_horario, fecha, horario_str, disponible = horario
    print(f"ID Horario: {id_horario}, Fecha: {fecha}, Horario: {horario_str}, Disponible: {disponible}")
    print("")

# Cerrar la conexión
cursor.close()
conn.close()
