import os
from datetime import datetime

# Carpeta que contiene los archivos .pos estos pueden ser las carpetas GEORED, POPASILP o SOAM
carpeta_archivos_pos = input("Ingrese la ruta de los datos gnss .pos (GEORED, POPASILP O SOAM): ")

# Encabezado para el nuevo archivo
encabezado = "Fecha\tX\tY\tZ\tSx\tSy\tSz\tRxy\tRxz\tRyz\tNLat\tElong\tHeight\tdN\tdE\tdU\tSn\tSe\tSu\tRne\tRnu\tReu\tSoln\n"

# Carpeta que contiene los archivos .txt de los datos de GEORED, POPASILP, SOAM
carpeta_salida_pos = input("Ingrese la ruta de salida de los datos procesados .pos: ")

# Iterar sobre todos los archivos .pos en la carpeta
for archivo_pos in os.listdir(carpeta_archivos_pos):
    if archivo_pos.endswith('.pos'):
        archivo_entrada = os.path.join(carpeta_archivos_pos, archivo_pos)
        archivo_salida = os.path.join(carpeta_archivos_pos, f'{archivo_pos.split(".")[0]}.txt')

        # Leer el archivo de entrada y escribir en el archivo de salida
        with open(archivo_entrada, 'r') as entrada, open(archivo_salida, 'w') as salida:
        
            salida.write(encabezado)
            # Copiar las líneas desde la línea 38
            lineas = entrada.readlines()[37:]

            # Escribir las líneas en el archivo de salida, eliminando las columnas 2 y 3 y convirtiendo la columna 1 a formato de fecha
            for linea in lineas:
                # Dividir la línea por espacios
                datos = linea.split()

                # Convertir la columna 1 a formato de fecha (YYYYMMDD)
                fecha = datetime.strptime(datos[0], '%Y%m%d').strftime('%d/%m/%Y')

                # Eliminar las columnas 2 y 3
                nueva_linea = '\t'.join([fecha] + datos[3:])

                # Escribir la nueva línea en el archivo de salida
                salida.write(nueva_linea + '\n')
                

        print(f'Datos del archivo {archivo_pos} procesados y guardados en {archivo_salida}')
