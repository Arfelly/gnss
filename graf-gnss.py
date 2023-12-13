import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
from datetime import datetime

carpeta = input("Ingrese la ruta de los archivos gnss .txt: ")
archivos = os.listdir(carpeta)

# Configurar límites de ejes Y
y_min, y_max = -0.06, 0.06

## Identificadores de archivos para los cuales agregar rectángulos
archivos_con_rectangulos = ["ABON", "BED1", "BED2", "BED3", "BED4", "BLAN", "BVTA", "CGR2", "COC2", "CURI", "GUAN", "LARO", "MINA",]  #este comentar

for archivo in archivos:
    if archivo.endswith('.txt'):
        # Leer datos desde el archivo
        ruta_archivo = os.path.join(carpeta, archivo)
        with open(ruta_archivo, 'r') as file:
            # Saltar la primera línea que contiene los encabezados
            next(file)
            fechas, dN, dE, dU = [], [], [], []
            for linea in file:
                valores = linea.split()
                fechas.append(datetime.strptime(valores[0], '%d/%m/%Y'))
                dN.append(float(valores[13]))  # Índice 13 para la columna 'dN'
                dE.append(float(valores[14]))  # Índice 14 para la columna 'dE'
                dU.append(float(valores[15]))  # Índice 15 para la columna 'dU'

        # Calcular el promedio móvil de cada 60 datos
        promedio_dN = np.convolve(dN, np.ones(60) / 60, mode='valid')
        promedio_dE = np.convolve(dE, np.ones(60) / 60, mode='valid')
        promedio_dU = np.convolve(dU, np.ones(60) / 60, mode='valid')

        # Crear el gráfico con tres subgráficos (uno para cada componente)
        fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=False)
        fig.suptitle(f'{archivo[:-4]}', y=0.92)

        # Configurar círculos para los datos en cada subgráfico
        axs[0].scatter(fechas, dN, color=(0,0,153 / 255), s=5, label='dN')
        axs[1].scatter(fechas, dE, color=(0,153 / 255,0), s=5, label='dE')
        axs[2].scatter(fechas, dU, color=(192 / 255,0,0), s=5, label='dU')

        # Configurar límites de ejes Y
        for ax in axs:
            ax.set_ylim(y_min, y_max)

        # Configurar ticks del eje X para mostrar solo algunas fechas
        ticks_cada_n = 200  # Mostrar una fecha por cada 200 días
        axs[0].set_xticks(fechas[::ticks_cada_n])
        axs[1].set_xticks(fechas[::ticks_cada_n])
        axs[2].set_xticks(fechas[::ticks_cada_n])

        # Configurar formato de fecha para mes-año
        date_format = DateFormatter('%b-%Y')
        axs[0].xaxis.set_major_formatter(date_format)
        axs[1].xaxis.set_major_formatter(date_format)
        axs[2].xaxis.set_major_formatter(date_format)

        # Configurar etiquetas
        axs[2].set_xlabel('Fecha')
        axs[0].set_ylabel(f'{archivo[:-4]} Norte')
        axs[1].set_ylabel(f'{archivo[:-4]} Este')
        axs[2].set_ylabel(f'{archivo[:-4]} Vertical')

        # Dibujar la línea punteada para el promedio móvil de cada 60 datos
        axs[0].plot(fechas, [np.nan]*59 + promedio_dN.tolist(), 'k--', alpha=0.3)
        axs[1].plot(fechas, [np.nan]*59 + promedio_dE.tolist(), 'k--', alpha=0.3)
        axs[2].plot(fechas, [np.nan]*59 + promedio_dU.tolist(), 'k--', alpha=0.3)
        
        if archivo[:-4] in archivos_con_rectangulos:# esto comentar
            # Definir el rango de fechas para el archivo actual
            erupcion = [datetime.strptime("28/03/2022", '%d/%m/%Y'), datetime.strptime("31/03/2022", '%d/%m/%Y')]
            aumento1 = [datetime.strptime("01/04/2022", '%d/%m/%Y'), datetime.strptime("14/01/2023", '%d/%m/%Y')]
            aumento2 = [datetime.strptime("15/01/2023", '%d/%m/%Y'), datetime.strptime("18/11/2023", '%d/%m/%Y')]
            for ax in axs:
                ax.axvspan(erupcion[0], erupcion[1], alpha=0.4, color='red')
                ax.axvspan(aumento1[0], aumento1[1], alpha=0.2, color='green')
                ax.axvspan(aumento2[0], aumento2[1], alpha=0.2, color='blue')

        
        directorio_salida = 'graficos_gnss'
        os.makedirs(directorio_salida, exist_ok = True)

        # Guardar el gráfico como un archivo PNG en el nuevo directorio
        ruta_guardado = os.path.join(directorio_salida, f'gráfico_{archivo[:-4]}.png')
        plt.savefig(ruta_guardado, bbox_inches='tight')

        # Cerrar el gráfico para liberar recursos
        plt.close()

print("Gráficos guardados exitosamente.")

##
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
from datetime import datetime

def cargar_datos_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        # Saltar la primera línea que contiene los encabezados
        next(file)
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

def configurar_ejes_y(axs, y_min, y_max):
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
        if archivo[:-4] in archivos_con_rectangulos:
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

def main():
    carpeta = input("Ingrese la ruta de los archivos GNSS .txt: ")
    archivos = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.txt')]
    
    y_min, y_max = -0.06, 0.06
    archivos_con_rectangulos = ["ABON", "BED1", "BED2", "BED3", "BED4", "BLAN", "BVTA", "CGR2", "COC2", "CURI", "GUAN", "LARO", "MINA"]

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta, archivo)
        fechas, dN, dE, dU = cargar_datos_desde_archivo(ruta_archivo)

        promedio_dN = calcular_promedio_movil(dN)
        promedio_dE = calcular_promedio_movil(dE)
        promedio_dU = calcular_promedio_movil(dU)

        fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=False)
        fig.suptitle(f'{archivo[:-4]}', y=0.92)

        configurar_grafico(axs[0], fechas, dN, f'{archivo[:-4]} Norte', (0,0,153/255))
        configurar_grafico(axs[1], fechas, dE, f'{archivo[:-4]} Este', (0,153/255,0))
        configurar_grafico(axs[2], fechas, dU, f'{archivo[:-4]} Vertical', (192/255,0,0))

        configurar_ejes_y(axs, y_min, y_max)
        configurar_ticks_y_formato_fecha(axs, fechas)
        dibujar_linea_punteada(axs[0], fechas, promedio_dN)
        dibujar_linea_punteada(axs[1], fechas, promedio_dE)
        dibujar_linea_punteada(axs[2], fechas, promedio_dU)
        dibujar_rectangulos(axs, fechas, archivos_con_rectangulos)

        directorio_salida = 'graficos_gnss'
        os.makedirs(directorio_salida, exist_ok=True)
        guardar_grafico(archivo, directorio_salida)

    print("Gráficos guardados exitosamente.")

if __name__ == "__main__":
    main()


