import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
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
            fecha = datetime.strftime(datos[0], '%Y%m%d')
            nueva_columna_fecha = '\t'.join([fecha] + datos[3:])
            salida.write(nueva_columna_fecha + '\n')

def procesar_archivo_pos(archivo_pos, carpeta_archivos_pos, carpeta_salida_pos):
    archivo_entrada = os.path.join(carpeta_archivos_pos, archivo_pos)
    archivo_salida = os.path.join(carpeta_salida_pos, f'{archivo_pos.split(".")[0]}.txt')

    encabezado = "Fecha\tX\tY\tZ\tSx\tSy\tSz\tRxy\tRxz\tRyz\tNLat\tElong\tHeight\tdN\tdE\tdU\tSn\tSe\tSu\tRne\tRnu\tReu\tSoln\n"

    lineas = leer_archivo_pos(archivo_entrada)
    escribir_archivo_txt(archivo_salida, encabezado, lineas)

    print(f'Datos del archivo {archivo_pos} procesados y guardados en {archivo_salida}')

def cargar_datos_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        next(file)  # Saltar la primera línea que contiene los encabezados
        fechas, dN, dE, dU = [], [], [], []
        for linea in file:
            valores = linea.split()
            fechas.append(datetime.strptime(valores[0], '%d/%m/%Y'))
            dN.append(float(valores[13]))  # Índice 13 para la columna 'dN'
            dE.append(float(valores[14]))  # Índice 14 para la columna 'dE'
            dU.append(float(valores[15]))  # Índice 15 para la columna 'dU'
    return fechas, dN, dE, dU

def calcular_promedio_movil(datos, ventana=60):
    return np.convolve(datos, np.ones(ventana) / ventana, mode='valid')

def configurar_grafico(ax, fechas, datos, nombre, color):
    ax.scatter(fechas, datos, color=color, s=5, label=nombre)

def configurar_ejes_y(axs):
    y_min, y_max = -0.06, 0.06
    for ax in axs:
        ax.set_ylim(y_min, y_max)

def configurar_ticks_y_formato_fecha(axs, fechas, ticks_cada_n=200):
    for ax in axs:
        ax.set_xticks(fechas[::ticks_cada_n])
        ax.xaxis.set_major_formatter(DateFormatter('%b-%Y'))

def dibujar_linea_punteada(ax, fechas, promedio_movil, alpha=0.3):
    ax.plot(fechas, [np.nan]*len(fechas) + promedio_movil.tolist(), 'k--', alpha=alpha)

def dibujar_rectangulos(axs, fechas, archivos_con_rectangulos):
    for archivo in archivos_con_rectangulos:
        if archivo.endswith('.txt'):
            # Leer datos desde el archivo
            ruta_archivo = os.path.join(carpeta_salida_pos, archivo)
            fechas, _, _, _ = cargar_datos_desde_archivo(ruta_archivo)

            if fechas:  # Verificar si se cargaron fechas correctamente
                # Definir el rango de fechas para el archivo actual
                erupcion = [datetime.strptime("28/03/2022", '%d/%m/%Y'), datetime.strptime("31/03/2022", '%d/%m/%Y')]
                aumento1 = [datetime.strptime("01/04/2022", '%d/%m/%Y'), datetime.strptime("14/01/2023", '%d/%m/%Y')]
                aumento2 = [datetime.strptime("15/01/2023", '%d/%m/%Y'), datetime.strptime("18/11/2023", '%d/%m/%Y')]

                for ax in axs:
                    ax.axvspan(erupcion[0], erupcion[1], alpha=0.4, color='red')
                    ax.axvspan(aumento1[0], aumento1[1], alpha=0.2, color='green')
                    ax.axvspan(aumento2[0], aumento2[1], alpha=0.2, color='blue')

def guardar_grafico(archivo, directorio_salida):
    ruta_guardado = os.path.join(directorio_salida, f'gráfico_{archivo[:-4]}.png')
    plt.savefig(ruta_guardado, bbox_inches='tight')
    plt.close()

def procesar_archivo_txt(archivo, carpeta_salida_pos, archivos_con_rectangulos):
    ruta_archivo = os.path.join(carpeta_salida_pos, archivo)
    fechas, dN, dE, dU = cargar_datos_desde_archivo(ruta_archivo)

    if fechas:  # Verificar si se cargaron fechas correctamente
        promedio_dN = calcular_promedio_movil(dN)
        promedio_dE = calcular_promedio_movil(dE)
        promedio_dU = calcular_promedio_movil(dU)

        fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=False)
        fig.suptitle(f'{archivo[:-4]}', y=0.92)

        configurar_grafico(axs[0], fechas, dN, f'{archivo[:-4]} Norte', (0,0,153/255))
        configurar_grafico(axs[1], fechas, dE, f'{archivo[:-4]} Este', (0,153/255,0))
        configurar_grafico(axs[2], fechas, dU, f'{archivo[:-4]} Vertical', (192/255,0,0))

        configurar_ejes_y(axs)
        configurar_ticks_y_formato_fecha(axs, fechas)
        dibujar_linea_punteada(axs[0], fechas, promedio_dN)
        dibujar_linea_punteada(axs[1], fechas, promedio_dE)
        dibujar_linea_punteada(axs[2], fechas, promedio_dU)
        dibujar_rectangulos(axs, fechas, archivos_con_rectangulos)
        
    directorio_salida = 'graficos_gnss'
    os.makedirs(directorio_salida, exist_ok=True)
    guardar_grafico(archivo, directorio_salida)

    print(f'Gráfico del archivo {archivo} generado y guardado.')


def main():
    carpeta_archivos_pos = input("Ingrese la ruta de los datos GNSS .pos (GEORED, POPASILP O SOAM): ")
    carpeta_salida_pos = input("Ingrese la ruta de salida de los datos procesados .pos: ")

    for archivo_pos in os.listdir(carpeta_archivos_pos):
        if archivo_pos.endswith('.pos'):
            procesar_archivo_pos(archivo_pos, carpeta_archivos_pos, carpeta_salida_pos)
            
            archivos_con_rectangulos = ["ABON", "BED1", "BED2", "BED3", "BED4", "BLAN", "BVTA", "CGR2", "COC2", "CURI", "GUAN", "LARO", "MINA"]
            
            procesar_archivo_txt(archivo_pos.split(".")[0] + ".txt", carpeta_salida_pos, archivos_con_rectangulos)

    print("Proceso completo. Gráficos y archivos TXT generados y guardados exitosamente.")

if __name__ == "__main__":
    main()