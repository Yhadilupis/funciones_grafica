import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cv2 as cv
import numpy as np
import os

def animar_y_grabar(x, y, nombre_video, lista_imagenes):
    fig, ax = plt.subplots()

    def actualizarPlot(i):
        ax.clear()
        ax.scatter(x[:i], y[:i])
        ax.set_xlim([1.1*np.min(x), 1.1*np.max(x)])
        ax.set_ylim([1.1*np.min(y), 1.1*np.max(y)])

        # Guardar cada frame como una imagen
        plt.savefig(f"frame_{i}.png")
        lista_imagenes.append(f"frame_{i}.png")

    animar = FuncAnimation(fig, actualizarPlot, range(
        len(x)), interval=0, cache_frame_data=False, repeat=False)
    animar.save(nombre_video, writer='ffmpeg', fps=30, dpi=100)

    plt.close(fig)

def generar_video_final(lista_videos, nombre_video_final):
    videos = []
    for video in lista_videos:
        videos.append(cv.VideoCapture(video))

    ancho = int(videos[0].get(cv.CAP_PROP_FRAME_WIDTH))
    alto = int(videos[0].get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(videos[0].get(cv.CAP_PROP_FPS))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video_combinado = cv.VideoWriter(
        nombre_video_final, fourcc, fps, (ancho, alto))

    # Unir todos los videos en uno solo
    for video in videos:
        while True:
            ret, frame = video.read()
            if not ret:
                break
            video_combinado.write(frame)

    # Cerrar todos los videos y el video combinado
    for video in videos:
        video.release()
    video_combinado.release()

    # Eliminar los archivos de video individuales
    for video_file in lista_videos:
        os.remove(video_file)

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


nombre_video_Seno = 'video_Seno.mp4'
nombre_video_Coseno = 'video_Coseno.mp4'
nombre_video_Logaritmo_Natural = 'video_Logaritmo_Natural.mp4'
nombre_video_Raíz_Cuadrada = 'video_Raíz_Cuadrada.mp4'

lista_videos = [nombre_video_Seno, nombre_video_Coseno, nombre_video_Logaritmo_Natural, nombre_video_Raíz_Cuadrada]
nombre_video_final = 'video_final.mp4'
generar_video_final(lista_videos, nombre_video_final)

reproducir_video(nombre_video_final)
