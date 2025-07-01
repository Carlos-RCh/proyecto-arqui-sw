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


cursor.execute("DROP SEQUENCE IF EXISTS usuario_id_seq CASCADE;")
# Crear tabla usuario
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('medico', 'paciente', 'administrativo', 'gestor'))
);
""")

# Crear tabla paciente
cursor.execute("""
CREATE TABLE IF NOT EXISTS paciente (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    seguro_medico TEXT CHECK (seguro_medico IN ('Fonasa', 'Isapre', 'Privado', 'Ninguno')),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);
""")

# Crear tabla medico (sin 'horarios_disponibles')
cursor.execute("""
CREATE TABLE IF NOT EXISTS medico (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    especialidad TEXT NOT NULL CHECK (especialidad IN ('Pediatria', 'Cardiologia', 'General', 'Dermatologia')),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);
""")

# Crear tabla horario con disponible como BOOLEAN
cursor.execute("""
CREATE TABLE IF NOT EXISTS horario (
    id SERIAL PRIMARY KEY,
    id_medico INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    horario TEXT NOT NULL,
    disponible BOOLEAN NOT NULL CHECK (disponible IN (TRUE, FALSE)),
    FOREIGN KEY (id_medico) REFERENCES medico(id) ON DELETE CASCADE
);
""")

# Crear tabla cita
cursor.execute("""
CREATE TABLE IF NOT EXISTS cita (
    id SERIAL PRIMARY KEY,
    id_horario INTEGER NOT NULL,
    estado TEXT NOT NULL CHECK (estado IN ('confirmada', 'cancelada','finalizada' )),
    id_paciente INTEGER NOT NULL,
    id_medico INTEGER NOT NULL,
    FOREIGN KEY (id_horario) REFERENCES horario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES medico(id) ON DELETE CASCADE
);
""")

# Crear tabla historia_clinica
cursor.execute("""
CREATE TABLE IF NOT EXISTS historia_clinica (
    id SERIAL PRIMARY KEY,
    id_paciente INTEGER NOT NULL,
    diagnostico TEXT,
    tratamiento TEXT,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id) ON DELETE CASCADE
);
""")

# Consultar todas las tablas existentes en la base de datos
cursor.execute("""
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
""")

# Obtener todas las tablas
tablas = cursor.fetchall()

# Imprimir las tablas
print("Tablas creadas en la base de datos:")
for tabla in tablas:
    print(tabla[0])


# Verificar si la tabla usuario está vacía
cursor.execute("SELECT COUNT(*) FROM usuario;")
cantidad_usuarios = cursor.fetchone()[0]

if cantidad_usuarios == 0:
    # Crear usuarios de prueba
    cursor.execute("""
    INSERT INTO usuario (nombre, correo, contrasena, rol)
    VALUES ('Gestor Sistema', 'gestor@gmail.com', '123', 'gestor');
    """)
    cursor.execute("""
        INSERT INTO usuario (nombre, correo, contrasena, rol)
        VALUES ('Carlos Ruiz', 'carlos@gmail.com', '123', 'medico');
    """)
    cursor.execute("""
        INSERT INTO usuario (nombre, correo, contrasena, rol)
        VALUES ('Nicolas Fernandez', 'nicolas@gmail.com', '123', 'medico');
    """)
    cursor.execute("""
        INSERT INTO usuario (nombre, correo, contrasena, rol)
        VALUES ('Luciano Zuñiga', 'luciano@gmail.com', '123', 'administrativo');
    """)
    cursor.execute("""
        INSERT INTO usuario (nombre, correo, contrasena, rol)
        VALUES ('Amanda Giovanini', 'amanda@gmail.com', '123', 'paciente');
    """)
    cursor.execute("""
        INSERT INTO usuario (nombre, correo, contrasena, rol)
        VALUES ('Jorge Gonzales', 'jorge@gmail.com', '123', 'paciente');
    """)

    # Insertar en tabla medico
    cursor.execute("SELECT id FROM usuario WHERE rol = 'medico';")
    medicos = cursor.fetchall()
    for medico in medicos:
        cursor.execute("""
            INSERT INTO medico (id_usuario, especialidad)
            VALUES (%s, %s);
        """, (medico[0], 'General'))

    # Insertar en tabla paciente
    cursor.execute("SELECT id FROM usuario WHERE rol = 'paciente';")
    pacientes = cursor.fetchall()
    for paciente in pacientes:
        cursor.execute("""
            INSERT INTO paciente (id_usuario, seguro_medico)
            VALUES (%s, %s);
        """, (paciente[0], 'Fonasa'))

    # Insertar horarios
    cursor.execute("SELECT id FROM medico;")
    medicos = cursor.fetchall()
    for medico in medicos:
        cursor.execute("""
            INSERT INTO horario (id_medico, fecha, horario, disponible)
            VALUES (%s, %s, %s, %s);
        """, (medico[0], '01/06', '12:00', True))
        cursor.execute("""
            INSERT INTO horario (id_medico, fecha, horario, disponible)
            VALUES (%s, %s, %s, %s);
        """, (medico[0], '02/06', '14:00', True))

    # Insertar historia clínica
    cursor.execute("SELECT id FROM paciente;")
    pacientes = cursor.fetchall()
    for paciente in pacientes:
        cursor.execute("""
            INSERT INTO historia_clinica (id_paciente, diagnostico, tratamiento)
            VALUES (%s, %s, %s);
        """, (paciente[0], 'Alergia estacional', 'Antihistamínicos'))
        cursor.execute("""
            INSERT INTO historia_clinica (id_paciente, diagnostico, tratamiento)
            VALUES (%s, %s, %s);
        """, (paciente[0], 'Gastritis', 'Antiácidos,Dieta blanda'))


# Confirmar y cerrar
conn.commit()
cursor.close()
conn.close()
