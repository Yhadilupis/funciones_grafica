import tkinter as tk
from tkinter import ttk
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cv2 as cv
import os

def animar_y_grabar(x, y, nombre_video):
    fig, ax = plt.subplots()

    def actualizarPlot(i):
        ax.clear()
        ax.scatter(x[:i], y[:i])
        ax.set_xlim([1.1*np.min(x), 1.1*np.max(x)])
        ax.set_ylim([1.1*np.min(y), 1.1*np.max(y)])
        plt.savefig(f"frame_{i}.png")

    animar = FuncAnimation(fig, actualizarPlot, range(len(x)), interval=0, cache_frame_data=False, repeat=False)
    animar.save(nombre_video, writer='ffmpeg', fps=30, dpi=100)
    plt.close(fig)

    # Eliminar las imágenes generadas después de crear el video
    for i in range(len(x)):
        os.remove(f"frame_{i}.png")

def generar_video_final(lista_imagenes, nombre_video_final):
    imagenes = [cv.imread(imagen) for imagen in lista_imagenes]

    ancho, alto, _ = imagenes[0].shape
    fps = 30
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video_final = cv.VideoWriter(nombre_video_final, fourcc, fps, (ancho, alto))

    for imagen in imagenes:
        video_final.write(imagen)

    video_final.release()

    for imagen_file in lista_imagenes:
        os.remove(imagen_file)

def reproducir_video(nombre_video):
    video = cv.VideoCapture(nombre_video)
    while True:
        ret, frame = video.read()
        if not ret:
            break
        cv.imshow('Video Final', frame)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    video.release()
    cv.destroyAllWindows()

def calcular_y_values(x_values, seleccion):
    if seleccion == "Seno":
        return np.sin(x_values)
    elif seleccion == "Coseno":
        return np.cos(x_values)
    elif seleccion == "Exponencial":
        return np.exp(x_values)
    elif seleccion == "Logaritmo Natural":
        return np.log(x_values)
    elif seleccion == "Raíz Cuadrada":
        return np.sqrt(x_values)
    else:
        return np.zeros_like(x_values)

def generar_y_grabar_video(seleccion_funcion, x_min, x_max, nombre_video):
    x_values = np.linspace(x_min, x_max, 100)
    y_values = calcular_y_values(x_values, seleccion_funcion)
    animar_y_grabar(x_values, y_values, nombre_video)

# Interfaz gráfica con Tkinter
def crear_interfaz_grafica():
    def calcular_y_grabar():
        seleccion_funcion = funcion_combobox.get()
        x_min = float(x_min_entry.get())
        x_max = float(x_max_entry.get())
        nombre_video = f"video_{seleccion_funcion}.mp4"
        
        generar_y_grabar_video(seleccion_funcion, x_min, x_max, nombre_video)
        reproducir_video(nombre_video)

    ventana = tk.Tk()
    ventana.title("Generación de Videos")

    funcion_label = tk.Label(ventana, text="Seleccione una función:")
    funcion_label.pack(pady=10)

    funciones_disponibles = ["Seno", "Coseno", "Exponencial", "Logaritmo Natural", "Raíz Cuadrada"]
    funcion_combobox = ttk.Combobox(ventana, values=funciones_disponibles, state="readonly")
    funcion_combobox.pack(pady=10)
    funcion_combobox.set(funciones_disponibles[0])

    x_limits_frame = tk.Frame(ventana)
    x_limits_frame.pack(pady=10)

    x_min_label = tk.Label(x_limits_frame, text="X mínimo:")
    x_min_label.grid(row=0, column=0)

    x_min_entry = tk.Entry(x_limits_frame)
    x_min_entry.grid(row=0, column=1)

    x_max_label = tk.Label(x_limits_frame, text="X máximo:")
    x_max_label.grid(row=0, column=2)

    x_max_entry = tk.Entry(x_limits_frame)
    x_max_entry.grid(row=0, column=3)

    calcular_button = tk.Button(ventana, text="Calcular y Grabar", command=calcular_y_grabar)
    calcular_button.pack(pady=10)

    ventana.mainloop()

crear_interfaz_grafica()
