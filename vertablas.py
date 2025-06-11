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

cursor.execute("SELECT * FROM usuario;")
usuarios = cursor.fetchall()
print("Usuarios:")
for u in usuarios:
    print(u)



cursor.execute("SELECT * FROM paciente;")
pacientes = cursor.fetchall()
print("Pacientes:")
for p in pacientes:
    print(p)
