'''
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
'''
###
import os
from datetime import datetime

def leer_archivo_pos(archivo_entrada):
    with open(archivo_entrada, 'r') as entrada:
        # Leer líneas desde la línea 38
        lineas_lec = entrada.readlines()[37:]
    return lineas_lec

def escribir_archivo_txt(archivo_salida, encabezado, lineas_lec):
    with open(archivo_salida, 'w') as salida:
        salida.write(encabezado)
        for linea in lineas_lec:
            datos = linea.split()
            fecha = datetime.strptime(datos[0], '%Y%m%d').strftime('%d/%m/%Y')
            nueva_columna_fecha = '\t'.join([fecha] + datos[3:])
            salida.write(nueva_columna_fecha + '\n')

def procesar_archivo_pos(archivo_pos, carpeta_archivos_pos, carpeta_salida_pos):
    archivo_entrada = os.path.join(carpeta_archivos_pos, archivo_pos)
    archivo_salida = os.path.join(carpeta_salida_pos, f'{archivo_pos.split(".")[0]}.txt')

    encabezado = "Fecha\tX\tY\tZ\tSx\tSy\tSz\tRxy\tRxz\tRyz\tNLat\tElong\tHeight\tdN\tdE\tdU\tSn\tSe\tSu\tRne\tRnu\tReu\tSoln\n"

    lineas = leer_archivo_pos(archivo_entrada)
    escribir_archivo_txt(archivo_salida, encabezado, lineas)

    print(f'Datos del archivo {archivo_pos} procesados y guardados en {archivo_salida}')

def main():
    carpeta_archivos_pos = input("Ingrese la ruta de los datos GNSS .pos (GEORED, POPASILP O SOAM): ")
    carpeta_salida_pos = input("Ingrese la ruta de salida de los datos procesados .pos: ")

    for archivo_pos in os.listdir(carpeta_archivos_pos):
        if archivo_pos.endswith('.pos'):
            procesar_archivo_pos(archivo_pos, carpeta_archivos_pos, carpeta_salida_pos)
            
            #archivos_con_rectangulos = ["ABON", "BED1", "BED2", "BED3", "BED4", "BLAN", "BVTA", "CGR2", "COC2", "CURI", "GUAN", "LARO", "MINA"]
            
            #procesar_archivo_txt(archivo_pos.split(".")[0] + ".#txt", carpeta_salida_pos, archivos_con_rectangulos)

    print("Proceso completo. Gráficos y archivos TXT generados y guardados exitosamente.")

if __name__ == "__main__":
    main()

