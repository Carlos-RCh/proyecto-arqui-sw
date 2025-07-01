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

# Obtener médicos con sus nombres
cursor.execute("""
    SELECT medico.id, usuario.nombre
    FROM medico
    JOIN usuario ON medico.id_usuario = usuario.id;
""")
medicos = cursor.fetchall()

print(f"Médicos: ")
print(f" ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ")
# Para cada médico, mostrar sus horarios
for id_medico, nombre in medicos:
    print(f" {nombre}")
    cursor.execute("""
        SELECT fecha, horario, disponible
        FROM horario
        WHERE id_medico = %s;
    """, (id_medico,))
    horarios = cursor.fetchall()
    
    for fecha, horario_str, disponible in horarios:
        print(f" - Fecha: {fecha}, Horario: {horario_str}, Disponible: {disponible}")
    
    print("")

# Cerrar la conexión
cursor.close()
conn.close()
