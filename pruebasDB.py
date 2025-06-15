import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="consultorio",
    user="carlos",
    password="213207091",
    host="localhost",
    port="6000"
)
cursor = conn.cursor()

# Solicitar el id_usuario del médico
id_usuario = 4

# Obtener el id_medico usando el id_usuario
cursor.execute("SELECT id FROM medico WHERE id_usuario = %s", (id_usuario,))
id_medico = cursor.fetchone()

if id_medico:
    id_medico = id_medico[0]
    print(f"ID Médico: {id_medico}")
    
    # Obtener todos los horarios del médico (sin importar el estado de disponibilidad)
    cursor.execute("""
    SELECT fecha, horario, disponible 
    FROM horario 
    WHERE id_medico = %s
    """, (id_medico,))
    
    horarios = cursor.fetchall()
    
    # Mostrar los horarios
    if horarios:
        print("Horarios registrados para el médico:")
        for horario in horarios:
            estado = "Disponible" if horario[2] else "No disponible"  # Esto es solo informativo
            print(f"Fecha: {horario[0]}, Hora: {horario[1]}, Estado: {estado}")
    else:
        print("No hay horarios registrados para este médico.")
else:
    print("El médico con este id_usuario no existe.")

# Cerrar la conexión
cursor.close()
conn.close()
