import tkinter as tk
from tkinter import ttk, messagebox
from Mapa import Mapa
from AEstrella import AEstrella

class InterfazMetro:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro CDMX - Planificador de Rutas")
        self.root.geometry("1100x750")
        
        # --- Lógica ---
        self.mapa_logico = Mapa()
        self.buscador = AEstrella(self.mapa_logico)
        self.modo_oscuro = False  # Estado inicial del tema

        # --- Paletas de Colores (Tema Claro / Oscuro) ---
        self.temas = {
            "claro": {
                "bg_app": "#f4f4f4",       # Fondo general
                "bg_panel": "#ffffff",     # Panel lateral
                "fg_text": "#333333",      # Texto principal
                "bg_canvas": "#ffffff",    # Fondo del mapa
                "linea_base": "#e0e0e0",   # Color de túneles inactivos
                "estacion_fill": "white",  # Relleno de puntos
                "estacion_outline": "#555",# Borde de puntos
                "ruta_color": "#007AFF",   # Azul brillante para la ruta
                "ruta_nodo": "#FFD700"     # Amarillo para nodos ruta
            },
            "oscuro": {
                "bg_app": "#1e1e1e",
                "bg_panel": "#2d2d2d",
                "fg_text": "#ffffff",
                "bg_canvas": "#1e1e1e",
                "linea_base": "#404040",
                "estacion_fill": "#2d2d2d",
                "estacion_outline": "#888",
                "ruta_color": "#00E5FF",   # Cian neón
                "ruta_nodo": "#FF3366"     # Rosa neón
            }
        }

        # --- Colores Oficiales de Líneas ---
        self.colores_lineas = {
            "L1": "#E81F76",   # Rosa Mexicano (Color oficial actual L1)
            "L3": "#95C11E",   # Verde Olivo
            "L7": "#F37735",   # Naranja
            "L9": "#5B3A29",   # Marrón
            "L12": "#C09928"   # Oro
        }

        # --- Coordenadas Visuales (Mismas que antes) ---
        self.coords_gui = {
            "Barranca_del_Muerto_L7": (150, 600), "Mixcoac_L7": (150, 540),
            "San_Antonio_L7": (150, 480), "San_Pedro_de_los_Pinos_L7": (150, 420),
            "Tacubaya_L7": (150, 360), "Constituyentes_L7": (150, 260),
            "Auditorio_L7": (150, 200), "Polanco_L7": (150, 140),
            
            "Observatorio_L1": (80, 410), "Tacubaya_L1": (150, 360),
            "Juanacatlan_L1": (230, 280), "Chapultepec_L1": (290, 220),
            "Sevilla_L1": (350, 220), "Insurgentes_L1": (410, 220),
            "Cuauhtemoc_L1": (470, 220), "Balderas_L1": (530, 220),

            "Tacubaya_L9": (150, 360), "Patriotismo_L9": (230, 360),
            "Chilpancingo_L9": (310, 360), "Centro_Medico_L9": (390, 360),
            "Lazaro_Cardenas_L9": (470, 360),

            "Universidad_L3": (390, 680), "Copilco_L3": (390, 640),
            "Miguel_Angel_de_Quevedo_L3": (390, 600), "Viveros_L3": (390, 560),
            "Coyoacan_L3": (390, 520), "Zapata_L3": (390, 480),
            "Division_del_Norte_L3": (390, 440), "Eugenia_L3": (390, 400),
            "Etiopia_L3": (390, 360), "Centro_Medico_L3": (390, 360),
            "Hospital_General_L3": (390, 300), "Ninos_Heroes_L3": (460, 260),
            "Balderas_L3": (530, 220), "Juarez_L3": (530, 160),

            "Mixcoac_L12": (150, 540), "Insurgentes_Sur_L12": (230, 540),
            "Hospital_20_de_Noviembre_L12": (310, 540), "Zapata_L12": (390, 480),
            "Parque_de_los_Venados_L12": (470, 540), "Eje_Central_L12": (550, 540),
        }

        # --- Configuración de Estilos (ttk) ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # Tema más moderno y plano
        
        # Configurar Interfaz
        self.crear_widgets()
        self.aplicar_tema() # Aplicar colores iniciales

    def crear_widgets(self):
        # 1. Panel Lateral (Control)
        self.frame_control = tk.Frame(self.root, width=300)
        self.frame_control.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_control.pack_propagate(False) # Evita que se encoja

        # Título
        self.lbl_titulo = tk.Label(self.frame_control, text="METRO CDMX", font=("Helvetica", 16, "bold"))
        self.lbl_titulo.pack(pady=(30, 20))

        # Buscadores
        self.lbl_origen = tk.Label(self.frame_control, text="Origen", font=("Arial", 10))
        self.lbl_origen.pack(pady=(10, 2), padx=20, anchor="w")
        
        self.combo_origen = ttk.Combobox(self.frame_control, font=("Arial", 11))
        self.combo_origen.pack(pady=0, padx=20, fill=tk.X)

        self.lbl_destino = tk.Label(self.frame_control, text="Destino", font=("Arial", 10))
        self.lbl_destino.pack(pady=(15, 2), padx=20, anchor="w")
        
        self.combo_destino = ttk.Combobox(self.frame_control, font=("Arial", 11))
        self.combo_destino.pack(pady=0, padx=20, fill=tk.X)

        # Cargar datos
        nodos = sorted(list(self.mapa_logico.get_grafo().nodes()))
        self.combo_origen['values'] = nodos
        self.combo_destino['values'] = nodos

        # Botón Calcular (Estilizado)
        self.btn_calcular = tk.Button(
            self.frame_control, 
            text="CALCULAR RUTA", 
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.calcular_ruta
        )
        self.btn_calcular.pack(pady=30, padx=20, fill=tk.X, ipady=5)

        # Resultados
        self.lbl_resultado = tk.Label(self.frame_control, text="", justify=tk.LEFT, anchor="nw", font=("Consolas", 10))
        self.lbl_resultado.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Botón Tema (Abajo)
        self.btn_tema = tk.Button(self.frame_control, text="Cambiar Tema 🌙/☀️", command=self.cambiar_tema, cursor="hand2", relief="flat")
        self.btn_tema.pack(side=tk.BOTTOM, pady=20)

        # 2. Área del Mapa (Canvas)
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_tema()

    def aplicar_tema(self):
        """Aplica los colores según el modo actual a toda la interfaz."""
        t = self.temas["oscuro"] if self.modo_oscuro else self.temas["claro"]

        # 1. Configurar widgets estándar
        self.root.config(bg=t["bg_app"])
        self.frame_control.config(bg=t["bg_panel"])
        self.canvas.config(bg=t["bg_canvas"])
        
        # Etiquetas y Textos
        labels = [self.lbl_titulo, self.lbl_origen, self.lbl_destino, self.lbl_resultado]
        for lbl in labels:
            lbl.config(bg=t["bg_panel"], fg=t["fg_text"])

        # Botones
        if self.modo_oscuro:
            self.btn_calcular.config(bg="#00E5FF", fg="black", activebackground="#00B2CC")
            self.btn_tema.config(bg="#444", fg="white")
            
            # Estilo Combobox Oscuro (Truco ttk)
            self.style.map('TCombobox', fieldbackground=[('readonly', '#444')])
            self.style.configure('TCombobox', foreground='black') 
        else:
            self.btn_calcular.config(bg="#007AFF", fg="white", activebackground="#005BBB")
            self.btn_tema.config(bg="#ddd", fg="black")
            
            self.style.map('TCombobox', fieldbackground=[('readonly', 'white')])

        # 2. Redibujar el mapa con los nuevos colores
        self.dibujar_mapa()

    def dibujar_mapa(self):
        """Dibuja el mapa completo. Si hay una ruta activa, la repinta."""
        self.canvas.delete("all")
        t = self.temas["oscuro"] if self.modo_oscuro else self.temas["claro"]
        grafo = self.mapa_logico.get_grafo()

        # Dibujar Conexiones (Túneles)
        for u, v in grafo.edges():
            if u in self.coords_gui and v in self.coords_gui:
                x1, y1 = self.coords_gui[u]
                x2, y2 = self.coords_gui[v]
                
                linea_u = u.split('_')[-1]
                linea_v = v.split('_')[-1]
                
                # Color de la línea o gris si es transbordo/base
                color = self.colores_lineas.get(linea_u, t["linea_base"]) if linea_u == linea_v else t["linea_base"]
                width = 3 if linea_u == linea_v else 1
                
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, tags="mapa_base")

        # Dibujar Estaciones (Puntos pequeños)
        r = 4 # Radio más pequeño (antes era 6 u 8)
        for nodo in grafo.nodes():
            if nodo in self.coords_gui:
                x, y = self.coords_gui[nodo]
                self.canvas.create_oval(
                    x-r, y-r, x+r, y+r, 
                    fill=t["estacion_fill"], 
                    outline=t["estacion_outline"], 
                    width=1,
                    tags="nodo"
                )

    def calcular_ruta(self):
        start = self.combo_origen.get()
        end = self.combo_destino.get()

        if not start or not end:
            messagebox.showwarning("Faltan datos", "Selecciona origen y destino.")
            return

        # Limpiar rutas previas
        self.canvas.delete("ruta_animada")
        self.canvas.delete("nodo_ruta")

        # Calcular lógica
        ruta, costo = self.buscador.encontrar_ruta(start, end)

        if not ruta:
            self.lbl_resultado.config(text="⚠️ No hay ruta disponible.")
            return

        # Mostrar texto
        pasos_str = " -> ".join([p.split('_')[0] for p in ruta])
        info = f"🛤️ RUTA ÓPTIMA\n\n📍 Origen: {start.split('_')[0]}\n🏁 Destino: {end.split('_')[0]}\n\n📏 Costo: {int(costo)} (aprox. m)\n\n📝 Pasos:\n{pasos_str}"
        self.lbl_resultado.config(text=info)

        # Iniciar Animación
        self.animar_ruta(ruta, 0)

    def animar_ruta(self, ruta, index):
        """Dibuja la ruta tramo por tramo recursivamente."""
        if index >= len(ruta) - 1:
            # Fin de la animación, resaltar nodos finales
            self.resaltar_nodos_ruta(ruta)
            return

        u, v = ruta[index], ruta[index+1]
        t = self.temas["oscuro"] if self.modo_oscuro else self.temas["claro"]
        
        if u in self.coords_gui and v in self.coords_gui:
            x1, y1 = self.coords_gui[u]
            x2, y2 = self.coords_gui[v]
            
            # Dibujar tramo grueso y brillante
            self.canvas.create_line(
                x1, y1, x2, y2, 
                fill=t["ruta_color"], 
                width=5, 
                capstyle=tk.ROUND,
                tags="ruta_animada"
            )
        
        # Llamar al siguiente paso en 60ms
        self.root.after(60, lambda: self.animar_ruta(ruta, index + 1))

    def resaltar_nodos_ruta(self, ruta):
        """Pinta los puntos de la ruta al final de la animación."""
        t = self.temas["oscuro"] if self.modo_oscuro else self.temas["claro"]
        r = 5
        for nodo in ruta:
            if nodo in self.coords_gui:
                x, y = self.coords_gui[nodo]
                # Efecto de 'brillo'
                self.canvas.create_oval(
                    x-r, y-r, x+r, y+r, 
                    fill=t["ruta_nodo"], 
                    outline=t["bg_app"], # Borde del color del fondo para contraste
                    width=2,
                    tags="nodo_ruta"
                )

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazMetro(root)
    root.mainloop()