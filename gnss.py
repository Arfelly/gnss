import subprocess

# Nombre del archivo .bat que deseas ejecutar
archivo_bat1 = "buscar_gnss.bat"
archivo_bat2 = "graf-gnss.bat"

# Ejecutar el primer archivo .bat
subprocess.run([archivo_bat1])

# Ejecutar el segundo archivo .bat
subprocess.run([archivo_bat2])
