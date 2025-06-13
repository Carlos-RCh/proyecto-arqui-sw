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

# Crear tabla medico 
cursor.execute("""
CREATE TABLE IF NOT EXISTS medico (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    especialidad TEXT NOT NULL CHECK (especialidad IN ('Pediatria', 'Cardiologia', 'General', 'Dermatologa')),
    horarios_disponibles JSON,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);
""")
print("Tabla 'medico' creada")

# Confirmar y cerrar
conn.commit()
cursor.close()
conn.close()
