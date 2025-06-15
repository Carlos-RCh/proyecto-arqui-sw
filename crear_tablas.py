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
print("Tabla 'usuario' creada")

# Crear tabla paciente
cursor.execute("""
CREATE TABLE IF NOT EXISTS paciente (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    seguro_medico TEXT CHECK (seguro_medico IN ('Fonasa', 'Isapre', 'Privado', 'Ninguno')),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);
""")
print("Tabla 'paciente' creada")

# Crear tabla medico (sin 'horarios_disponibles')
cursor.execute("""
CREATE TABLE IF NOT EXISTS medico (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    especialidad TEXT NOT NULL CHECK (especialidad IN ('Pediatria', 'Cardiologia', 'General', 'Dermatologia')),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);
""")
print("Tabla 'medico' creada")

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
print("Tabla 'horario' creada")


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
print("Tabla 'cita' creada")


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
print("Tabla 'historia_clinica' creada")


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


# Confirmar y cerrar
conn.commit()
cursor.close()
conn.close()
