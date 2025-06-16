import subprocess
import time
import sys

servicios = [
    "agenda_medica.py",
    "autenticacion.py",
    "gestion_citas.py",
    "gestion_usuarios.py",
    "historia_clinica.py",
    "registro_usuario.py"
]

for servicio in servicios:
    print(f"Iniciando: {servicio}")
    subprocess.Popen([sys.executable, f"Servicios/{servicio}"])
    time.sleep(2)  # Esperar 2 segundos antes de iniciar el siguiente

# Esperar confirmación del usuario antes de cerrar
input("\nTodos los servicios han sido lanzados. Presiona Enter para finalizar este script...")
