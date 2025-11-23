import tkinter as tk
from tkinter import ttk, messagebox
from Mapa import Mapa
from AEstrella import AEstrella

class InterfazMetro:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo de Ruta Óptima - Metro CDMX")
        self.root.geometry("1000x700")
        
        # 1. Inicializar la lógica
        self.mapa_logico = Mapa()
        self.buscador = AEstrella(self.mapa_logico)
        
        # -----------------------------------------------------------
        # 2. CONFIGURACIÓN VISUAL (Colores y Coordenadas de Pantalla)
        # -----------------------------------------------------------
        self.colores_lineas = {
            "L1": "#800000",   # Granate [cite: 7]
            "L3": "#95C11E",   # Verde claro [cite: 8]
            "L7": "#F37735",   # Naranja [cite: 8]
            "L9": "#5B3A29",   # Marrón [cite: 9]
            "L12": "#007A33"   # Verde oscuro [cite: 9]
        }

        # Coordenadas X, Y (pixels) para imitar el diagrama del PDF
        # Ajusta estos valores si quieres mover estaciones en la pantalla
        self.coords_gui = {
            # Línea 7 (Naranja) - Vertical izquierda
            "Barranca_del_Muerto_L7": (100, 550),
            "Mixcoac_L7": (100, 500),
            "San_Antonio_L7": (100, 450),
            "San_Pedro_de_los_Pinos_L7": (100, 400),
            "Tacubaya_L7": (100, 350),
            "Constituyentes_L7": (100, 250),
            "Auditorio_L7": (100, 200),
            "Polanco_L7": (100, 150),

            # Línea 1 (Granate) - Diagonal y Horizontal
            "Observatorio_L1": (50, 400), 
            "Tacubaya_L1": (100, 350), # Coincide con L7
            "Juanacatlan_L1": (180, 270),
            "Chapultepec_L1": (240, 210),
            "Sevilla_L1": (300, 210),
            "Insurgentes_L1": (360, 210),
            "Cuauhtemoc_L1": (420, 210),
            "Balderas_L1": (480, 210),

            # Línea 9 (Marrón) - Paralela a L1
            "Tacubaya_L9": (100, 350), # Coincide con L7 y L1
            "Patriotismo_L9": (180, 350),
            "Chilpancingo_L9": (260, 350),
            "Centro_Medico_L9": (340, 350),
            "Lazaro_Cardenas_L9": (420, 350),

            # Línea 3 (Verde Claro) - Vertical Derecha
            "Universidad_L3": (340, 650),
            "Copilco_L3": (340, 610),
            "Miguel_Angel_de_Quevedo_L3": (340, 570),
            "Viveros_L3": (340, 530),
            "Coyoacan_L3": (340, 490),
            "Zapata_L3": (340, 450),
            "Division_del_Norte_L3": (340, 410),
            "Eugenia_L3": (340, 380), # Curva leve
            "Etiopia_L3": (340, 350), # Cruza con L9 pero no hay transbordo
            "Centro_Medico_L3": (340, 350), # Transbordo L9
            "Hospital_General_L3": (340, 300),
            "Ninos_Heroes_L3": (410, 260), # Diagonal hacia Balderas
            "Balderas_L3": (480, 210),    # Transbordo L1
            "Juarez_L3": (480, 150),

            # Línea 12 (Verde Oscuro) - Horizontal Abajo
            "Mixcoac_L12": (100, 500), # Transbordo L7
            "Insurgentes_Sur_L12": (180, 500),
            "Hospital_20_de_Noviembre_L12": (260, 500),
            "Zapata_L12": (340, 450), # Transbordo L3 - Conecta en diagonal
            "Parque_de_los_Venados_L12": (420, 500),
            "Eje_Central_L12": (500, 500),
        }

        # -----------------------------------------------------------
        # 3. INTERFAZ GRÁFICA (WIDGETS)
        # -----------------------------------------------------------
        
        # Panel de Control (Izquierda)
        self.frame_control = tk.Frame(root, padx=10, pady=10, bg="#f0f0f0")
        self.frame_control.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.frame_control, text="Estación Origen:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(20, 5))
        self.combo_origen = ttk.Combobox(self.frame_control, width=25)
        self.combo_origen.pack()

        tk.Label(self.frame_control, text="Estación Destino:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=(20, 5))
        self.combo_destino = ttk.Combobox(self.frame_control, width=25)
        self.combo_destino.pack()

        self.btn_calcular = tk.Button(self.frame_control, text="CALCULAR RUTA", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), command=self.calcular_ruta)
        self.btn_calcular.pack(pady=30)

        self.lbl_resultado = tk.Label(self.frame_control, text="Resultados aparecerán aquí", bg="white", relief=tk.SUNKEN, width=30, height=15, wraplength=200, justify=tk.LEFT, anchor="nw")
        self.lbl_resultado.pack(pady=10)

        # Cargar estaciones en los combobox
        nodos_ordenados = sorted(list(self.mapa_logico.get_grafo().nodes()))
        self.combo_origen['values'] = nodos_ordenados
        self.combo_destino['values'] = nodos_ordenados

        # Panel del Mapa (Derecha)
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Dibujar el mapa base al iniciar
        self.dibujar_mapa_base()

    def dibujar_mapa_base(self):
        """Dibuja todas las líneas y estaciones estáticas."""
        grafo = self.mapa_logico.get_grafo()
        
        # 1. Dibujar conexiones (túneles)
        for u, v, data in grafo.edges(data=True):
            if u in self.coords_gui and v in self.coords_gui:
                x1, y1 = self.coords_gui[u]
                x2, y2 = self.coords_gui[v]
                
                # Determinar color de la línea
                linea_u = u.split('_')[-1] # Obtiene "L1" de "Balderas_L1"
                linea_v = v.split('_')[-1]
                
                color = "#999999" # Color por defecto (gris)
                width = 4
                
                if linea_u == linea_v:
                    # Es una conexión normal de línea
                    color = self.colores_lineas.get(linea_u, "black")
                else:
                    # Es un transbordo
                    color = "black"
                    width = 2
                    # Dibujar línea punteada para transbordos si quieres
                    # self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, dash=(4, 2))
                    # continue 

                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle=tk.ROUND)

        # 2. Dibujar Estaciones (nodos)
        r = 6 # Radio del círculo
        for nodo in grafo.nodes():
            if nodo in self.coords_gui:
                x, y = self.coords_gui[nodo]
                # Círculo blanco con borde negro (estilo metro clásico)
                self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="black", width=2)
                
                # Etiqueta de nombre (opcional, puede saturar)
                nombre_limpio = nodo.split('_')[0]
                # self.canvas.create_text(x+10, y, text=nombre_limpio, anchor="w", font=("Arial", 8))

    def calcular_ruta(self):
        start = self.combo_origen.get()
        end = self.combo_destino.get()

        if not start or not end:
            messagebox.showwarning("Error", "Por favor selecciona ambas estaciones.")
            return

        # Limpiar mapa (redibujar base)
        self.canvas.delete("ruta") # Borra solo elementos etiquetados como ruta
        self.dibujar_mapa_base() # O simplemente repintar encima

        # Obtener ruta de A*
        ruta, costo = self.buscador.encontrar_ruta(start, end)

        if not ruta:
            self.lbl_resultado.config(text="No se encontró ruta.")
            return

        # Mostrar texto
        texto_res = f"Ruta Óptima:\n\nOrigen: {start}\nDestino: {end}\n\n"
        texto_res += f"Costo total: {int(costo)} m\n\nPasos:\n"
        for i, paso in enumerate(ruta):
            texto_res += f"{i+1}. {paso}\n"
        
        self.lbl_resultado.config(text=texto_res)

        # DIBUJAR RUTA (RESALTADO)
        self.resaltar_ruta(ruta)

    def resaltar_ruta(self, ruta):
        """Dibuja la ruta calculada en color brillante sobre el mapa."""
        # 1. Resaltar aristas
        for i in range(len(ruta) - 1):
            u = ruta[i]
            v = ruta[i+1]
            if u in self.coords_gui and v in self.coords_gui:
                x1, y1 = self.coords_gui[u]
                x2, y2 = self.coords_gui[v]
                # Línea gruesa azul cian brillante
                self.canvas.create_line(x1, y1, x2, y2, fill="#00FFFF", width=6, capstyle=tk.ROUND, tags="ruta")

        # 2. Resaltar nodos de la ruta
        r = 8
        for nodo in ruta:
            if nodo in self.coords_gui:
                x, y = self.coords_gui[nodo]
                # Punto amarillo brillante
                self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="yellow", outline="black", width=2, tags="ruta")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazMetro(root)
    root.mainloop()