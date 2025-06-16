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

# Obtener el id del medico desde la tabla medico usando el id_usuario
cursor.execute("SELECT id FROM medico WHERE id_usuario = %s", (6,))
id_medico = cursor.fetchone()[0]  # Asumiendo que el ID de usuario 6 es 'medico1'

# Crear 3 horarios para 'medico1'
horarios = [
    ("06/01", "09:00-10:00", True),  # Fecha, hora, disponible
    ("06-02", "10:00-11:00", True),
    ("06/03", "14:00-15:00", True)
]

# Insertar los horarios en la tabla horario
for horario in horarios:
    fecha, hora, disponible = horario
    cursor.execute("""
        INSERT INTO horario (id_medico, fecha, horario, disponible)
        VALUES (%s, %s, %s, %s)
    """, (id_medico, fecha, hora, disponible))

conn.commit()

print(f"Se crearon {len(horarios)} horarios para el medico con ID {id_medico}")

# Cerrar la conexión
cursor.close()
conn.close()
