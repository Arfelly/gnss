#Elaborado por Arfelly Donato Caro, actualizaciones en el repo https://github.com/Arfelly/gnss, contacto:arfelly23@gmail.com
#Fecha 06 de julio de 2024 V1.2

'''Lector y graficador de archivos .pos'''

import os
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

root = tk.Tk()
root.withdraw()

HEADER = "Fecha\tX\tY\tZ\tSx\tSy\tSz\tRxy\tRxz\tRyz\tNLat\tElong\tHeight\tdN\tdE\tdU\tSn\tSe\tSu\tRne\tRnu\tReu\tSoln\n"
RECTANGLE_DATES = [
    ("28/03/2022", "31/03/2022", 0.4, 'red'),
    ("01/04/2022", "14/01/2023", 0.2, 'green')
]

def leer_archivo_pos(ruta_entrada):
    with open(ruta_entrada, 'r') as entrada:
        lineas = entrada.readlines()[37:]
    return lineas

def escribir_archivo_txt(ruta_salida, encabezado, lineas):
    with open(ruta_salida, 'w') as salida:
        salida.write(encabezado)
        for linea in lineas:
            datos = linea.split()
            fecha = datetime.strptime(datos[0], '%Y%m%d').strftime('%d/%m/%Y')
            nueva_columna_fecha = '\t'.join([fecha] + datos[3:])
            salida.write(nueva_columna_fecha + '\n')

def procesar_archivo_pos(archivo_pos, carpeta_entrada, carpeta_salida_txt):
    ruta_entrada = os.path.join(carpeta_entrada, archivo_pos)
    ruta_salida = os.path.join(carpeta_salida_txt, f'{archivo_pos.split(".")[0]}.txt')

    lineas = leer_archivo_pos(ruta_entrada)
    escribir_archivo_txt(ruta_salida, HEADER, lineas)

    print(f'Datos del archivo {archivo_pos} procesados y guardados en {ruta_salida}')

def cargar_datos_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        next(archivo)
        fechas, dN, dE, dU, Sn, Se, Su = [], [], [], [], [], [], []
        for linea in archivo:
            valores = linea.split()
            fechas.append(datetime.strptime(valores[0], '%d/%m/%Y'))
            dN.append(float(valores[13]))
            dE.append(float(valores[14]))
            dU.append(float(valores[15]))
            Sn.append(float(valores[16]))
            Se.append(float(valores[17]))
            Su.append(float(valores[18]))
    return fechas, dN, dE, dU, Sn, Se, Su

def calcular_promedio_movil(datos, ventana=60):
    promedio_movil = []
    for i in range(len(datos) - ventana + 1):
        promedio_movil.append(sum(datos[i:i + ventana]) / ventana)
    return promedio_movil

def configurar_grafico(ax, fechas, datos, titulo, color, mostrar_barras_error=True, errores=None):
    ax.scatter(fechas, datos, s=5, label=titulo, color=color)

    if mostrar_barras_error and errores is not None:
        ax.errorbar(fechas, datos, yerr=errores, markersize=3, fmt='o', label=titulo, color=color, capsize=1, ecolor='k', alpha=0.1)
    
    ax.set_ylabel(titulo, fontsize=18)

def configurar_ejes_y(axs):
    y_min, y_max = -0.06, 0.06
    for ax in axs:
        ax.set_ylim(y_min, y_max)

def configurar_ticks_y_formato_fecha(axs, fechas, ticks_cada_n=200):
    for ax in axs:
        ax.set_xticks(fechas[::ticks_cada_n])
        ax.xaxis.set_major_formatter(DateFormatter('%b-%Y'))
        ax.xaxis.set_tick_params(labelsize=12)

def dibujar_linea_punteada(ax, fechas, promedio_movil, alpha=0.3):
    nan_list = [float('nan')] * 59
    promedio_movil_list = nan_list + promedio_movil
    ax.plot(fechas, promedio_movil_list, 'k--', alpha=alpha)

def dibujar_rectangulos(axs, fechas, carpeta_salida, archivos_con_rectangulos):
    for archivo in archivos_con_rectangulos:
        if archivo.endswith('.txt'):
            ruta_archivo = os.path.join(carpeta_salida, archivo)
            fechas_archivo, _, _, _, _, _, _ = cargar_datos_desde_archivo(ruta_archivo)

            if fechas_archivo:
                fecha_final = fechas_archivo[-1].strftime('%d/%m/%Y')
                rect_dates = RECTANGLE_DATES + [("15/01/2023", fecha_final, 0.2, 'blue')]

                for inicio, fin, alpha, color in rect_dates:
                    inicio_dt = datetime.strptime(inicio, '%d/%m/%Y')
                    fin_dt = datetime.strptime(fin, '%d/%m/%Y')
                    for ax in axs:
                        ax.axvspan(inicio_dt, fin_dt, alpha=alpha, color=color)

def procesar_archivo_txt(archivo, carpeta_salida_txt, nombre_carpeta_entrada, carpeta_salida_graficos, archivos_con_rectangulos, mostrar_barras_error):
    ruta_archivo = os.path.join(carpeta_salida_txt, archivo)
    
    fechas, dN, dE, dU, Sn, Se, Su = cargar_datos_desde_archivo(ruta_archivo)

    if fechas:
        promedio_dN = calcular_promedio_movil(dN)
        promedio_dE = calcular_promedio_movil(dE)
        promedio_dU = calcular_promedio_movil(dU)

        directorio_graficos = os.path.join(carpeta_salida_graficos, f'Graficos_GNSS_{nombre_carpeta_entrada}')
        os.makedirs(directorio_graficos, exist_ok=True)

        fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=False)
        fig.suptitle(f'{archivo[:-4]}', y=0.92, fontsize=26)

        configurar_grafico(axs[0], fechas, dN, f'{archivo[:-4]} Norte', (0, 0, 153/255), mostrar_barras_error, errores=Sn)
        configurar_grafico(axs[1], fechas, dE, f'{archivo[:-4]} Este', (0, 153/255, 0), mostrar_barras_error, errores=Se)
        configurar_grafico(axs[2], fechas, dU, f'{archivo[:-4]} Vertical', (192/255, 0, 0), mostrar_barras_error, errores=Su)

        configurar_ejes_y(axs)
        configurar_ticks_y_formato_fecha(axs, fechas)
        dibujar_linea_punteada(axs[0], fechas, promedio_dN)
        dibujar_linea_punteada(axs[1], fechas, promedio_dE)
        dibujar_linea_punteada(axs[2], fechas, promedio_dU)

        if archivo in archivos_con_rectangulos:
            dibujar_rectangulos(axs, fechas, carpeta_salida_txt, [archivo])

        nombre_grafico = f'Gráfico_{nombre_carpeta_entrada}_{archivo[:-4]}.png'
        ruta_grafico = os.path.join(directorio_graficos, nombre_grafico)
        plt.savefig(ruta_grafico, bbox_inches='tight')
        
        plt.close()

        print(f'Gráfico del archivo {archivo} generado y guardado en {ruta_grafico}.')

def main():
    print('Lector y graficador de archivos .pos')
    carpeta_archivos_pos = filedialog.askdirectory(title="Ingrese la ruta de los datos GNSS .pos (GEORED, POPASILP O SOAM): ")
    nombre_carpeta_entrada = os.path.basename(os.path.normpath(carpeta_archivos_pos))
    carpeta_salida_txt = os.path.join(carpeta_archivos_pos, f'Archivos_GNSS_{nombre_carpeta_entrada}')
    carpeta_salida_graficos = carpeta_archivos_pos

    os.makedirs(carpeta_salida_txt, exist_ok=True)

    respuesta_usuario = messagebox.askyesno(title="Barras de error", message="¿Graficar con barras de error?")
    mostrar_barras_error = respuesta_usuario 

    archivos_con_rectangulos = ["ABON.txt", "BED1.txt", "BED2.txt", "BED3.txt", "BED4.txt", "BLAN.txt", "BVTA.txt", "CGR2.txt", "COC2.txt", "CURI.txt", "GUAN.txt", "LARO.txt", "MINA.txt"]

    archivos_pos = [archivo for archivo in os.listdir(carpeta_archivos_pos) if archivo.endswith('.pos')]

    progress = tk.Toplevel()
    progress.title("Progreso")
    progress.geometry("300x100")

    tk.Label(progress, text="Procesando archivos...").pack(pady=10)
    barra_progreso = ttk.Progressbar(progress, orient="horizontal", length=250, mode="determinate")
    barra_progreso.pack(pady=10)
    barra_progreso["maximum"] = len(archivos_pos)

    root.update()

    for i, archivo_pos in enumerate(archivos_pos):
        procesar_archivo_pos(archivo_pos, carpeta_archivos_pos, carpeta_salida_txt)
        procesar_archivo_txt(archivo_pos.split(".")[0] + ".txt", carpeta_salida_txt, nombre_carpeta_entrada, carpeta_salida_graficos, archivos_con_rectangulos, mostrar_barras_error)
        barra_progreso["value"] = i + 1
        root.update_idletasks()

    progress.destroy()

    messagebox.showinfo(title="Proceso completo", message=f"Los gráficos y archivos .txt se han generado y guardado en:\n\n{carpeta_archivos_pos}\n\n")

    root.destroy()
    

if __name__ == "__main__":
    main()


