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

# Consultar todos los médicos
cursor.execute("""
SELECT m.id, u.nombre, m.especialidad, m.horarios_disponibles
FROM medico m
JOIN usuario u ON m.id_usuario = u.id
""")

# Obtener todos los resultados
medicos = cursor.fetchall()

# Mostrar los médicos con sus especialidades y horarios disponibles
print("Médicos registrados:")
for medico in medicos:
    id_medico = medico[0]
    nombre_usuario = medico[1]
    especialidad = medico[2]
    horarios_disponibles = medico[3]  # No es necesario usar json.loads()

    print(f"ID Médico: {id_medico}")
    print(f"Nombre: {nombre_usuario}")
    print(f"Especialidad: {especialidad}")
    print(f"Horarios Disponibles:")
    for dia, horarios in horarios_disponibles.items():
        print(f"  {dia}: {', '.join(horarios)}")
    print("-" * 50)

# Cerrar conexión
cursor.close()
conn.close()
