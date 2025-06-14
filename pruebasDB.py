import psycopg2
import json

# Conectar a la base de datos
conn = psycopg2.connect(
    dbname="consultorio", 
    user="carlos", 
    password="213207091", 
    host="localhost", 
    port="6000"
)
cursor = conn.cursor()

# ID del médico que deseas consultar
id_medico = 9  # Aquí va el ID del médico

# Obtener los horarios disponibles del médico por ID
cursor.execute("SELECT horarios_disponibles FROM medico WHERE id_usuario = %s", (id_medico,))
result = cursor.fetchone()

if result and result[0]:
    # Verificar si el valor ya es una lista (si ya está deserializado)
    if isinstance(result[0], str):  # Si es un string, entonces debemos cargarlo con json
        horarios = json.loads(result[0])
    else:
        horarios = result[0]  # Si ya es una lista, no es necesario cargarlo con json

    print("Horarios disponibles del médico:")
    for horario in horarios:
        print(f"Fecha: {horario['fecha']}, Hora: {horario['hora']}")
else:
    print("El médico no tiene horarios disponibles registrados o no se encontró el médico con ese ID.")

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()
