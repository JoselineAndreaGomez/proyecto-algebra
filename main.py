from tkinter import Tk, Label, Button
import tkinter as tk
from math import sqrt
from tkinter import messagebox
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def clear(x_entries, y_entries, z_entries, graph_window=None):
    """Limpia los campos de entrada y cierra la ventana del gráfico si existe."""
    for entry in x_entries:
        entry.delete(0, tk.END)
    for entry in y_entries:
        entry.delete(0, tk.END)
    for entry in z_entries:
        entry.delete(0, tk.END)
    
    # Cerrar la ventana del gráfico si se ha pasado
    if graph_window:
        graph_window.destroy()

def process_entries(x_entries, y_entries, z_entries):
    """Procesa las entradas y muestra las columnas de puntos."""
    points = []
    try:
        for i in range(6):  # Asegurarse de recorrer las 6 aeronaves
            x = float(x_entries[i].get())
            y = float(y_entries[i].get())
            z = float(z_entries[i].get())
            points.append((x, y, z))
        
        # Crear dos columnas
        columna_1 = points[0:3]  # Resultados del 1 al 3
        columna_2 = points[3:6]  # Resultados del 4 al 6

        # Imprimir resultados
        print("Columna 1: ", columna_1)
        print("Columna 2: ", columna_2)
        
        # Limpiar las entradas después de procesar
        clear(x_entries, y_entries, z_entries)
        
        # Llamar a la función para mostrar el gráfico
        show_graph(columna_1, columna_2)
    except ValueError:
        print("Por favor, introduce números válidos en todos los campos.")

def show_graph(columna_1, columna_2):
    """Muestra el gráfico en una nueva ventana."""
    graph_window = tk.Toplevel()
    graph_window.title("Gráfico de Aeronaves")

    # Aquí puedes agregar el código para dibujar el gráfico
    # Este es un ejemplo de cómo cerrar la ventana del gráfico al salir
    graph_window.protocol("WM_DELETE_WINDOW", lambda: clear([], [], [], graph_window))
def new_window():
    for widget in main_window.winfo_children():
        widget.destroy()
    
    label = tk.Label(main_window, text="Posiciòn de las aeronaves")
    label.pack(pady=20)

    

    main_frame = tk.Frame(main_window)
    main_frame.pack(pady=5)
    

    # Frame para la columna izquierda
    left_frame = tk.Frame(main_frame)
    left_frame.grid(row=0, column=0, padx=(0, 150))  # Añadir espacio a la derecha

    # Frame para la columna derecha
    right_frame = tk.Frame(main_frame)
    right_frame.grid(row=0, column=1)

    x_entries = []
    y_entries = []
    z_entries = []

    def add_aeronave(frame, num, row):
        aeronave_label = tk.Label(frame, text=f"Aeronave {num}:")
        aeronave_label.grid(row=row, column=0, columnspan=2, pady=(5, 0))

        x_label = tk.Label(frame, text="x:")
        x_label.grid(row=row + 1, column=0, padx=5, sticky='e')  # Alinear a la derecha
        x_entry = tk.Entry(frame, width=10)
        x_entry.grid(row=row + 1, column=1, padx=5)

        y_label = tk.Label(frame, text="y:")
        y_label.grid(row=row + 2, column=0, padx=5, sticky='e')  # Alinear a la derecha
        y_entry = tk.Entry(frame, width=10)
        y_entry.grid(row=row + 2, column=1, padx=5)

        z_label = tk.Label(frame, text="z:")
        z_label.grid(row=row + 3, column=0, padx=5, sticky='e')  # Alinear a la derecha
        z_entry = tk.Entry(frame, width=10)
        z_entry.grid(row=row + 3, column=1, padx=5)

        x_entries.append(x_entry)
        y_entries.append(y_entry)
        z_entries.append(z_entry)
    for i in range(1, 4):  # Aeronaves 1 a 3
        add_aeronave(left_frame, i, (i - 1) * 4)

    # Agregar aeronaves 4 y 5 en la columna derecha
    for i in range(4, 7):  # Aeronaves 4 y 5
        add_aeronave(right_frame, i, (i - 4) * 4)


    global frame_plot
    frame_plot = tk.Frame(main_window)
    frame_plot.pack(pady=10)


    # CALCULAR LA DISTANCIA ENTRE AERONAVES
    def submit_data():
        points = []  # Lista para almacenar las coordenadas de las aeronaves
        distances = []
        labels = []

        for i in range(6):  # Asegurarse de recorrer las 5 aeronaves
            x = float(x_entries[i].get())
            y = float(y_entries[i].get())
            z = float(z_entries[i].get())
            points.append((x, y, z))

        # Calcular distancias entre cada par de aeronaves
        for i in range(len(points)):
            for j in range(len(points)):
                if i != j:  # Asegurarse de no calcular la distancia de una aeronave consigo misma
                    p1 = points[i]
                    p2 = points[j]
                    distance = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)
                    distances.append(distance)
                    labels.append(f"AERONAVE {i + 1} - AERONAVE {j + 1}")  # Etiqueta de distancia

        # Crear una nueva ventana para mostrar las etiquetas
        result_window = tk.Toplevel(main_window)
        result_window.title("Resultados de Distancias")

        distances_frame = tk.Frame(result_window)
        distances_frame.pack(pady=10)

        left_frame = tk.Frame(distances_frame)
        left_frame.pack(side='left', padx=10)

        right_frame = tk.Frame(distances_frame)
        right_frame.pack(side='right', padx=10)

        for i, distance in enumerate(distances):
            color = "green"  # Color por defecto
            if distance <= 9:
                color = "red"   # Peligro
            elif distance <= 15:
                color = "yellow"  # Precaución
            elif distance > 20:
                color = "green"  # Normal

            # Crear un label para cada distancia en su propio frame
            label_frame = left_frame if i % 2 == 0 else right_frame

            label = tk.Label(label_frame, text=f"{labels[i]}: {distance:.2f} km", bg=color, fg="black", width=35)
            label.pack(fill='x')

        # Botón para generar gráfico
        generate_graph_button = tk.Button(result_window, text="Generar Gráfico", command=lambda: scatter_plot(points))
        generate_graph_button.pack(pady=10)

    

    def scatter_plot(points):
        # Descomponer los puntos en listas de coordenadas x, y, z
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        z_coords = [p[2] for p in points]

        # Crear el gráfico de dispersión
        plt.figure(figsize=(8, 6))
        plt.scatter(x_coords, y_coords, c=z_coords, cmap='viridis', s=100)  # Cambia el tamaño y el color según la coordenada z
        plt.colorbar(label='Altura (Z)')
        plt.title('Gráfico de Dispersión de Aeronaves')
        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.grid(True)

        # Agregar etiquetas con el número de cada aeronave
        for i, (x, y) in enumerate(zip(x_coords, y_coords)):
            plt.text(x, y, f'Aeronave {i + 1}', fontsize=9, ha='right', va='bottom')

        plt.show()

    # Botón para enviar y mostrar datos en la nueva ventana
    submit_button = tk.Button(main_window, text="Calcular distancias", command=submit_data)
    submit_button.pack(pady=10)

    clear_button=tk.Button(main_window, text="Limpiar", command=new_window)
    clear_button.pack(pady=10)

    volver_btn = tk.Button(main_window, text="Volver", command=volver_a_principal)
    volver_btn.pack(pady=10)



def volver_a_principal():
    for widget in main_window.winfo_children():
        widget.destroy()


    label = Label(main_window, text="Entrenamiento Primario de Técnicos Controladores Aéreos")
    label.grid(row=0, column=0, columnspan=2, pady=10)

    usuario_text = tk.Label(main_window, text="Usuario:")
    usuario_text.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
    usuario = tk.Entry(main_window, width=40)
    usuario.grid(row=1, column=1, padx=5, pady=10)

    password_text = tk.Label(main_window, text="Contraseña:")
    password_text.grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)
    password = tk.Entry(main_window, width=40, show='*')
    password.grid(row=2, column=1, padx=5, pady=10)

    button = Button(main_window, text="Iniciar Sesiòn", command=new_window)
    button.grid(row=3, columnspan=2, pady=10)


main_window = Tk()
main_window.title("EPTCA")
volver_a_principal()

main_window.mainloop()