import tkinter as tk
from tkinter import ttk, messagebox
import math

# Importamos tu lógica existente
from Mapa import Mapa
from AEstrella import AEstrella

# --- CLASE TOOLTIP (Ventana flotante) ---
# --- CLASE TOOLTIP (Ventana flotante) ---
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        if self.tipwindow or not text: return
        
        # Calcular posición basada únicamente en el ratón
        x = self.widget.winfo_pointerx() + 15
        y = self.widget.winfo_pointery() + 10
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1) # Quitar bordes de ventana
        tw.wm_geometry("+%d+%d" % (x, y))
        
        label = tk.Label(tw, text=text, justify=tk.LEFT,
                       background="#1F2937", fg="#F3F4F6",
                       relief=tk.SOLID, borderwidth=0,
                       font=("Segoe UI", 9), padx=8, pady=4)
        label.pack()

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw: tw.destroy()

# --- CLASE AUTOCOMPLETE COMBOBOX (Buscador Real) ---
class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, parent, lista_completa, **kwargs):
        super().__init__(parent, **kwargs)
        self._lista_completa = lista_completa
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._lista_completa

    def handle_keyrelease(self, event):
        # Teclas que no deben filtrar
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 'Return', 'Tab'):
            if event.keysym == 'BackSpace' and len(self.get()) == 0:
                 self['values'] = self._lista_completa # Restaurar si borra todo
            return

        valor_actual = self.get().lower()
        if valor_actual == '':
            self['values'] = self._lista_completa
        else:
            # Filtrar lista
            filtrada = [item for item in self._lista_completa if valor_actual in item.lower()]
            self['values'] = filtrada
            
            # Si hay resultados, desplegar lista
            if filtrada:
                self.event_generate('<Down>')

# --- CLASE BOTÓN MODERNO ---
class BotonModerno(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=50, bg_color="#2563EB", text_color="white", hover_color="#1D4ED8"):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        
        self.rect = self.create_rounded_rect(2, 2, width-2, height-2, 20, fill=bg_color, outline="")
        self.texto = self.create_text(width/2, height/2, text=text, fill=text_color, font=("Segoe UI", 11, "bold"))
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")

    def on_leave(self, e):
        self.itemconfig(self.rect, fill=self.bg_color)

    def on_click(self, e):
        if self.command: self.command()

    def update_colors(self, parent_bg, btn_bg, btn_hover):
        self.config(bg=parent_bg)
        self.bg_color = btn_bg
        self.hover_color = btn_hover
        self.itemconfig(self.rect, fill=btn_bg)

# --- INTERFAZ PRINCIPAL ---
class InterfazMetro2025:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro CDMX • Navigator 2025")
        self.root.geometry("1280x850")
        
        self.mapa_logico = Mapa()
        self.buscador = AEstrella(self.mapa_logico)
        self.modo_oscuro = True 
        
        # --- DATOS DE DIRECCIONES (Terminales aproximadas) ---
        # Ayuda a decidir "Dirección X" según si la coordenada aumenta o disminuye
        self.terminales = {
            "L1": {"izq": "Observatorio", "der": "Pantitlán"}, # Izq (Oeste), Der (Este)
            "L3": {"arriba": "Indios Verdes", "abajo": "Universidad"},
            "L7": {"arriba": "El Rosario", "abajo": "Barranca del Muerto"},
            "L9": {"izq": "Tacubaya", "der": "Pantitlán"},
            "L12": {"izq": "Mixcoac", "der": "Tláhuac"}
        }

        # Paletas
        self.colores = {
            "claro": {
                "bg_app": "#F3F4F6", "bg_panel": "#FFFFFF", 
                "text_primary": "#111827", "text_secondary": "#6B7280",
                "map_bg": "#FFFFFF", "line_inactive": "#E5E7EB", 
                "node_fill": "white", "node_outline": "#374151",
                "text_map": "#374151"
            },
            "oscuro": {
                "bg_app": "#0F172A", "bg_panel": "#1E293B", 
                "text_primary": "#F8FAFC", "text_secondary": "#94A3B8",
                "map_bg": "#0F172A", "line_inactive": "#334155",
                "node_fill": "#1E293B", "node_outline": "#94A3B8",
                "text_map": "#CBD5E1"
            }
        }
        
        self.lineas_color = {
            "L1": "#EC4899", "L3": "#84CC16", "L7": "#F97316", "L9": "#A97142", "L12": "#EAB308"
        }
        
        self.info_lineas = {
            "L1": "Línea 1", "L3": "Línea 3", "L7": "Línea 7", "L9": "Línea 9", "L12": "Línea 12"
        }

        # Preparar lista para el buscador
        self.display_map = {}
        for nodo in self.mapa_logico.get_grafo().nodes():
            nombre = nodo.split('_')[0]
            linea = nodo.split('_')[-1]
            nombre_display = f"{nombre} ({linea})"
            self.display_map[nombre_display] = nodo
        
        self.lista_estaciones = sorted(list(self.display_map.keys()))

        # Coordenadas GUI
        # --- COORDENADAS GUI CORREGIDAS (Cuadrícula Limpia) ---
        # Lógica:
        # Eje X: L7 en 150, L3 en 500
        # Eje Y: Tacubaya/L9 en 380, Zapata en 500, Mixcoac en 580
        
        self.coords_gui = {
            # --- LÍNEA 7 (Naranja) - Vertical Izquierda (Recta) ---
            "Barranca_del_Muerto_L7": (150, 720),
            "Mixcoac_L7": (150, 620),             # Transbordo L12
            "San_Antonio_L7": (150, 540),
            "San_Pedro_de_los_Pinos_L7": (150, 460),
            "Tacubaya_L7": (150, 380),            # Transbordo L1, L9 (Hub Central)
            "Constituyentes_L7": (150, 280),
            "Auditorio_L7": (150, 200),
            "Polanco_L7": (150, 120),

            # --- LÍNEA 1 (Rosa) - Diagonal Superior ---
            # Sale de Observatorio, baja a Tacubaya, sube diagonal a Balderas
            "Observatorio_L1": (60, 440),
            "Tacubaya_L1": (150, 380),            # Coincide con L7
            "Juanacatlan_L1": (230, 320),         # Diagonal subiendo
            "Chapultepec_L1": (300, 280),         # Diagonal subiendo
            "Sevilla_L1": (360, 280),             # Horizontal
            "Insurgentes_L1": (430, 280),
            "Cuauhtemoc_L1": (500, 280),
            "Balderas_L1": (580, 280),            # Transbordo L3 (Cruce arriba)

            # --- LÍNEA 9 (Marrón) - Horizontal Central (Recta) ---
            "Tacubaya_L9": (150, 380),            # Coincide con L7
            "Patriotismo_L9": (260, 380),
            "Chilpancingo_L9": (370, 380),
            "Centro_Medico_L9": (500, 380),       # Transbordo L3 (Importante alinear X con L3)
            "Lazaro_Cardenas_L9": (620, 380),

            # --- LÍNEA 3 (Verde) - Vertical Derecha (Recta) ---
            # Alineada en X=500 para cruzar con Centro Médico
            "Universidad_L3": (500, 750),
            "Copilco_L3": (500, 700),
            "Miguel_Angel_de_Quevedo_L3": (500, 650),
            "Viveros_L3": (500, 600),
            "Coyoacan_L3": (500, 550),
            "Zapata_L3": (500, 500),              # Transbordo L12
            "Division_del_Norte_L3": (500, 460),
            "Eugenia_L3": (500, 430),
            "Etiopia_L3": (500, 405),
            "Centro_Medico_L3": (500, 380),       # Cruce perfecto con L9
            "Hospital_General_L3": (500, 330),
            "Ninos_Heroes_L3": (540, 305),        # Pequeña curva para evitar solapamiento visual
            "Balderas_L3": (580, 280),            # Conecta con L1
            "Juarez_L3": (580, 200),              # Sube recto

            # --- LÍNEA 12 (Dorada) - Inferior ---
            "Mixcoac_L12": (150, 620),            # Coincide con L7
            "Insurgentes_Sur_L12": (240, 620),
            "Hospital_20_de_Noviembre_L12": (330, 620),
            "Zapata_L12": (500, 500),             # Diagonal directa a Zapata L3
            "Parque_de_los_Venados_L12": (600, 540), # Diagonal bajando
            "Eje_Central_L12": (680, 540),
        }

        self.crear_layout()
        self.aplicar_tema()

    def crear_layout(self):
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.main_container, width=400, padx=30, pady=30)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Header
        self.lbl_logo = tk.Label(self.sidebar, text="CDMX Metro", font=("Segoe UI Variable Display", 28, "bold"), anchor="w")
        self.lbl_logo.pack(fill=tk.X)
        self.lbl_sublogo = tk.Label(self.sidebar, text="Planificador Inteligente", font=("Segoe UI", 11), anchor="w")
        self.lbl_sublogo.pack(fill=tk.X, pady=(0, 40))

        # Buscadores con Autocomplete
        self.crear_autocomplete("Punto de Partida", "origen")
        tk.Frame(self.sidebar, height=20, bg=self.sidebar['bg']).pack()
        self.crear_autocomplete("Destino Final", "destino")

        # Botón
        tk.Frame(self.sidebar, height=40, bg=self.sidebar['bg']).pack()
        self.btn_calc = BotonModerno(self.sidebar, "Calcular Ruta Óptima", self.calcular_ruta, width=340, height=55)
        self.btn_calc.pack()

        # Resultados
        tk.Frame(self.sidebar, height=30, bg=self.sidebar['bg']).pack()
        self.lbl_res_titulo = tk.Label(self.sidebar, text="Detalles del viaje", font=("Segoe UI", 12, "bold"), anchor="w")
        self.lbl_res_titulo.pack(fill=tk.X, pady=(0, 10))

        self.txt_pasos = tk.Text(self.sidebar, height=15, font=("Segoe UI", 10), 
                                 relief="flat", wrap="word", padx=15, pady=15, 
                                 highlightthickness=0, state="disabled")
        self.txt_pasos.pack(fill=tk.BOTH, expand=True)
        self.configurar_tags_texto()

        # Botón Tema
        self.btn_tema = tk.Button(self.sidebar, text="Cambiar Tema 🌓", command=self.cambiar_tema, 
                                  relief="flat", cursor="hand2", font=("Segoe UI", 10))
        self.btn_tema.pack(side=tk.BOTTOM, anchor="w")

        # Mapa
        self.map_frame = tk.Frame(self.main_container)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.map_frame, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def crear_autocomplete(self, titulo, var_name):
        lbl = tk.Label(self.sidebar, text=titulo, font=("Segoe UI", 10, "bold"), anchor="w")
        lbl.pack(fill=tk.X, pady=(0, 8))
        if var_name == "origen": self.lbl_origen = lbl
        else: self.lbl_destino = lbl

        # Usar nuestra clase personalizada
        cb = AutocompleteCombobox(self.sidebar, self.lista_estaciones, font=("Segoe UI", 11))
        cb.pack(fill=tk.X, ipady=8) 
        
        if var_name == "origen": self.combo_origen = cb
        else: self.combo_destino = cb

    def configurar_tags_texto(self):
        self.txt_pasos.tag_config("titulo", font=("Segoe UI", 11, "bold"))
        self.txt_pasos.tag_config("meta", foreground="#888")
        self.txt_pasos.tag_config("direccion", foreground="#2563EB", font=("Segoe UI", 10, "bold"))
        self.txt_pasos.tag_config("transbordo", foreground="#EF4444", font=("Segoe UI", 10, "bold"))
        self.txt_pasos.tag_config("pasos", lmargin1=15, lmargin2=15)

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_tema()

    def aplicar_tema(self):
        t = self.colores["oscuro"] if self.modo_oscuro else self.colores["claro"]
        
        self.root.config(bg=t["bg_app"])
        self.main_container.config(bg=t["bg_app"])
        self.sidebar.config(bg=t["bg_panel"])
        self.map_frame.config(bg=t["map_bg"])
        self.canvas.config(bg=t["map_bg"])
        
        for l in [self.lbl_logo, self.lbl_res_titulo]: l.config(bg=t["bg_panel"], fg=t["text_primary"])
        for l in [self.lbl_sublogo, self.lbl_origen, self.lbl_destino, self.btn_tema]: l.config(bg=t["bg_panel"], fg=t["text_secondary"])

        self.txt_pasos.config(bg=t["bg_app"], fg=t["text_primary"])
        
        btn_bg = "#818CF8" if self.modo_oscuro else "#4F46E5"
        btn_hover = "#6366F1" if self.modo_oscuro else "#4338CA"
        self.btn_calc.update_colors(t["bg_panel"], btn_bg, btn_hover)

        self.dibujar_mapa()

    def dibujar_mapa(self):
        self.canvas.delete("all")
        t = self.colores["oscuro"] if self.modo_oscuro else self.colores["claro"]
        grafo = self.mapa_logico.get_grafo()

        # 1. DIBUJAR CONEXIONES (LÍNEAS)
        for u, v in grafo.edges():
            if u in self.coords_gui and v in self.coords_gui:
                x1, y1 = self.coords_gui[u]
                x2, y2 = self.coords_gui[v]
                linea_u = u.split('_')[-1]
                linea_v = v.split('_')[-1]
                
                # Definir grosor y color
                if linea_u == linea_v:
                    color = self.lineas_color.get(linea_u, "#999")
                    w = 6 # Línea gruesa para las rutas
                else:
                    color = t["line_inactive"]
                    w = 3 # Línea fina para transbordos
                
                # Dibujar línea redondeada
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=w, capstyle=tk.ROUND, tags="mapa")

        # 2. DIBUJAR ESTACIONES Y TEXTOS
        r = 7 # Radio del punto
        for nodo in grafo.nodes():
            if nodo in self.coords_gui:
                x, y = self.coords_gui[nodo]
                nombre_limpio = nodo.split('_')[0]
                linea = nodo.split('_')[-1]

                # --- Lógica de Posición del Texto ---
                # Por defecto, texto a la derecha
                offset_x = 18
                offset_y = -5
                anchor_pos = "w" # West (alineado a la izquierda del texto)
                
                # Si es la Línea 7 (Naranja vertical izquierda), poner texto a la izquierda
                # Excepción: Tacubaya y Mixcoac son cruces, mejor dejarlos a la derecha
                if "L7" in linea and "Tacubaya" not in nombre_limpio and "Mixcoac" not in nombre_limpio:
                    offset_x = -18
                    anchor_pos = "e" # East (alineado a la derecha del texto)

                # Si es Balderas o Juárez (extremo derecho), ajustar un poco
                if "Juarez" in nombre_limpio:
                    offset_y = -15
                    offset_x = 0

                # --- Dibujar Círculos ---
                # 1. Círculo externo (del color del fondo) para "recortar" la línea que pasa por debajo
                self.canvas.create_oval(x-(r+2), y-(r+2), x+(r+2), y+(r+2), fill=t["map_bg"], outline="", tags="mapa")
                
                # 2. Círculo interno (el nodo real)
                item_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=t["node_fill"], outline=t["node_outline"], width=1.5, tags=("nodo", nodo))

                # --- Dibujar Texto con Halo ---
                text_x = x + offset_x
                text_y = y + offset_y
                angle = 20 # Ángulo de inclinación
                
                # Halo (Borde grueso del color del fondo para que se lea sobre las líneas)
                self.canvas.create_text(text_x, text_y, text=nombre_limpio, anchor=anchor_pos, font=("Segoe UI", 8, "bold"), fill=t["map_bg"], width=150, angle=angle)
                self.canvas.create_text(text_x, text_y, text=nombre_limpio, anchor=anchor_pos, font=("Segoe UI", 8, "bold"), fill=t["map_bg"], width=150, angle=angle) # Doble pasada para más grosor
                
                # Texto Final
                self.canvas.create_text(text_x, text_y, text=nombre_limpio, anchor=anchor_pos, font=("Segoe UI", 8, "bold"), fill=t["text_map"], tags=("texto", nodo), angle=angle)

                # --- Bindings para Interactividad (Hover) ---
                self.canvas.tag_bind(item_id, "<Enter>", lambda e, n=nodo, i=item_id: self.on_hover_enter(e, n, i))
                self.canvas.tag_bind(item_id, "<Leave>", lambda e, i=item_id: self.on_hover_leave(e, i))

    def on_hover_enter(self, event, nodo_id, item_id):
        self.canvas.itemconfig(item_id, width=3, outline=self.colores["oscuro" if self.modo_oscuro else "claro"]["text_primary"])
        nombre = nodo_id.split('_')[0]
        linea = nodo_id.split('_')[-1]
        info = f"{nombre}\n{self.info_lineas.get(linea, linea)}"
        
        self.tooltip = ToolTip(self.canvas)
        self.tooltip.showtip(info)

    def on_hover_leave(self, event, item_id):
        t = self.colores["oscuro"] if self.modo_oscuro else self.colores["claro"]
        self.canvas.itemconfig(item_id, width=1.5, outline=t["node_outline"])
        if hasattr(self, 'tooltip'): self.tooltip.hidetip()

    def get_direccion_linea(self, u, v, linea):
        """Determina la dirección (terminal) basada en coordenadas GUI aproximadas"""
        if u not in self.coords_gui or v not in self.coords_gui: return ""
        if linea not in self.terminales: return ""
        
        xu, yu = self.coords_gui[u]
        xv, yv = self.coords_gui[v]
        
        # Lógica simple: Si aumenta X va a derecha, Si aumenta Y va abajo
        dx = xv - xu
        dy = yv - yu
        
        terms = self.terminales[linea]
        
        if linea in ["L1", "L9", "L12"]: # Horizontales
            return terms["der"] if dx > 0 else terms["izq"]
        elif linea in ["L3", "L7"]: # Verticales
            return terms["abajo"] if dy > 0 else terms["arriba"]
        return ""

    def calcular_ruta(self):
        origen_display = self.combo_origen.get()
        destino_display = self.combo_destino.get()

        if not origen_display or not destino_display:
            messagebox.showinfo("Ups", "Selecciona origen y destino.")
            return

        id_origen = self.display_map.get(origen_display)
        id_destino = self.display_map.get(destino_display)
        
        if not id_origen or not id_destino:
            messagebox.showerror("Error", "Estación no válida.")
            return

        ruta, costo_metros = self.buscador.encontrar_ruta(id_origen, id_destino)
        self.dibujar_mapa() # Reset
        
        if not ruta:
            self.mostrar_info("No se encontró ruta.")
            return

        # --- CÁLCULO DE TIEMPO REALISTA ---
        # Velocidad media Metro: ~35 km/h = ~580 m/min
        # Tiempo parada: 20-30 seg (0.5 min)
        # Tiempo transbordo: 4 min
        
        num_paradas = 0
        num_transbordos = 0
        
        linea_actual = ruta[0].split('_')[-1]
        
        for i in range(1, len(ruta)):
            linea_nueva = ruta[i].split('_')[-1]
            if linea_nueva != linea_actual:
                num_transbordos += 1
                linea_actual = linea_nueva
            else:
                num_paradas += 1
        
        tiempo_viaje = (costo_metros / 580) + (num_paradas * 0.5) + (num_transbordos * 4)
        tiempo_viaje = int(math.ceil(tiempo_viaje))

        self.mostrar_pasos_detallados(ruta, costo_metros, tiempo_viaje)
        self.animar_ruta(ruta, 0)

    def mostrar_pasos_detallados(self, ruta, distancia, tiempo):
        self.txt_pasos.config(state="normal")
        self.txt_pasos.delete(1.0, tk.END)
        
        self.txt_pasos.insert(tk.END, f"⏱ {tiempo} min total  |  📏 {int(distancia)} m\n\n", "titulo")

        # Control primer nodo
        nodo_inicio = ruta[0]
        nombre_inicio = nodo_inicio.split('_')[0]
        linea_actual = nodo_inicio.split('_')[-1]
        
        # Intentar predecir dirección inicial si hay más de 1 nodo
        dir_str = ""
        if len(ruta) > 1:
            dir_term = self.get_direccion_linea(ruta[0], ruta[1], linea_actual)
            if dir_term: dir_str = f"Dir. {dir_term}"

        self.txt_pasos.insert(tk.END, f"• Inicio en {nombre_inicio}\n", "pasos")
        if dir_str:
            self.txt_pasos.insert(tk.END, f"   → {self.info_lineas.get(linea_actual)} ({dir_str})\n", "direccion")
        
        count = 0
        
        for i in range(1, len(ruta)):
            nodo = ruta[i]
            linea = nodo.split('_')[-1]
            
            # Detectar cambio de linea
            if linea != linea_actual:
                # Escribir resumen anterior
                if count > 0: self.txt_pasos.insert(tk.END, f"   ↓  {count} estaciones\n", "meta")
                
                # Transbordo
                nombre_trans = nodo.split('_')[0]
                
                # CORRECCIÓN: Si el cambio de línea ocurre en el índice 1 (al principio)
                # y es el mismo nombre de estación, NO es un viaje, es que empezamos en el nodo incorrecto del transbordo
                if i == 1 and nombre_trans == nombre_inicio:
                    # Simplemente actualizar la línea actual sin imprimir "Transbordo"
                    linea_actual = linea
                    # Recalcular dirección
                    if i+1 < len(ruta):
                        dir_term = self.get_direccion_linea(ruta[i], ruta[i+1], linea)
                        if dir_term: 
                             self.txt_pasos.insert(tk.END, f"   → Cambio a {self.info_lineas.get(linea)} (Dir. {dir_term})\n", "direccion")
                    continue

                self.txt_pasos.insert(tk.END, f"• TRANSBORDO en {nombre_trans}\n", "transbordo")
                
                # Dirección nueva línea
                if i+1 < len(ruta):
                    dir_term = self.get_direccion_linea(ruta[i], ruta[i+1], linea)
                    if dir_term:
                        self.txt_pasos.insert(tk.END, f"   → {self.info_lineas.get(linea)} (Dir. {dir_term})\n", "direccion")
                
                linea_actual = linea
                count = 0
            else:
                count += 1
        
        if count > 0: self.txt_pasos.insert(tk.END, f"   ↓  {count} estaciones\n", "meta")
        self.txt_pasos.insert(tk.END, f"🏁 Llegada a {ruta[-1].split('_')[0]}", "titulo")
        self.txt_pasos.config(state="disabled")

    def mostrar_info(self, texto):
        self.txt_pasos.config(state="normal")
        self.txt_pasos.delete(1.0, tk.END)
        self.txt_pasos.insert(tk.END, texto)
        self.txt_pasos.config(state="disabled")

    def animar_ruta(self, ruta, index):
        if index >= len(ruta) - 1: return
        u, v = ruta[index], ruta[index+1]
        if u in self.coords_gui and v in self.coords_gui:
            x1, y1 = self.coords_gui[u]
            x2, y2 = self.coords_gui[v]
            color = "#22D3EE" if self.modo_oscuro else "#0284C7"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=4, capstyle=tk.ROUND)
        self.root.after(60, lambda: self.animar_ruta(ruta, index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    app = InterfazMetro2025(root)
    root.mainloop()