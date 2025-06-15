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
    # ID del usuario (Carlos Ruiz)
    id_usuario = 1  # Suponiendo que el ID de usuario es 1 para "Carlos Ruiz"

    # Obtener el id_paciente del usuario
    cursor.execute("""
    SELECT id FROM paciente WHERE id_usuario = %s
    """, (id_usuario,))
    id_paciente = cursor.fetchone()

    if id_paciente:
        id_paciente = id_paciente[0]  # Extraer el id_paciente
        print(f"ID del paciente: {id_paciente}")

        # Insertar tres casos de historia clínica para el paciente
        cursor.execute("""
        INSERT INTO historia_clinica (id_paciente, diagnostico, tratamiento)
        VALUES (%s, %s, %s)
        """, (id_paciente, 'gripe', 'reposo'))

        cursor.execute("""
        INSERT INTO historia_clinica (id_paciente, diagnostico, tratamiento)
        VALUES (%s, %s, %s)
        """, (id_paciente, 'dolor de cabeza', 'analgésicos'))

        cursor.execute("""
        INSERT INTO historia_clinica (id_paciente, diagnostico, tratamiento)
        VALUES (%s, %s, %s)
        """, (id_paciente, 'fiebre', 'paracetamol'))

        # Confirmar los cambios
        conn.commit()

        print("3 casos de historia clínica creados para el paciente con ID:", id_paciente)
    else:
        print("No se encontró el paciente con el id_usuario:", id_usuario)

finally:
    # Cerrar conexión
    cursor.close()
    conn.close()
