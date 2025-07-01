import subprocess
import time
import sys

servicios = [
    "agenda_medica.py",
    "autenticacion.py",
    "gestion_citas.py",
    "gestion_usuarios.py",
    "historia_clinica.py",
    "notificacion.py",
    "registro_usuario.py",
    "reporte.py"
]

# Guardar procesos en una lista
procesos = []

for servicio in servicios:
    proceso = subprocess.Popen([sys.executable, f"Servicios/{servicio}"])
    procesos.append(proceso)
    time.sleep(2)  # Esperar 2 segundos antes de iniciar el siguiente

# Esperar confirmación del usuario antes de cerrar
input("\nTodos los servicios han sido lanzados (Presiona Enter para detenerlos)...")

# Terminar todos los procesos
for proceso in procesos:
    proceso.terminate()
