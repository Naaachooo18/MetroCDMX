import tkinter as tk
from tkinter import ttk, messagebox
import math

# Importamos tu lógica existente
from Mapa import Mapa
from AEstrella import AEstrella

# --- CLASE TOOLTIP ---
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        if self.tipwindow or not text: return
        x = self.widget.winfo_pointerx() + 15
        y = self.widget.winfo_pointery() + 10
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
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

# --- CLASE AUTOCOMPLETE COMBOBOX (CORREGIDA: NO BLOQUEA ESCRITURA) ---
class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, parent, lista_completa, **kwargs):
        super().__init__(parent, **kwargs)
        self._lista_completa = lista_completa
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._lista_completa

    def handle_keyrelease(self, event):
        # Ignorar teclas de navegación y enter
        if event.keysym in ('Up', 'Down', 'Return', 'Tab', 'Left', 'Right', 'Home', 'End', 'Prior', 'Next'):
            return

        # 1. Guardar posición exacta del cursor
        try:
            cursor_pos = self.index(tk.INSERT)
        except:
            cursor_pos = 0
        
        valor_actual = self.get()
        
        # Filtrar lista
        if valor_actual == '':
            self['values'] = self._lista_completa
        else:
            filtrada = [item for item in self._lista_completa if valor_actual.lower() in item.lower()]
            self['values'] = filtrada
            
            # Gestionar desplegable
            if filtrada:
                self.tk.call('ttk::combobox::Post', self._w)
            else:
                self.tk.call('ttk::combobox::Unpost', self._w)
        
        # 2. CRÍTICO: Restaurar estado de escritura
        try:
            self.icursor(cursor_pos)      # Poner cursor donde estaba
            self.selection_clear()        # Quitar selección azul (que borraba el texto)
            self.focus_set()              # Forzar foco en el texto, no en la lista
        except:
            pass
        

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
        
        # ESTILO CLAM (MODERNO)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.mapa_logico = Mapa()
        self.buscador = AEstrella(self.mapa_logico)
        self.modo_oscuro = True 
        
        # Checkbox Hora Punta
        self.hora_punta_var = tk.BooleanVar()
        self.hora_punta_var.set(False)

        # NOMBRES MAPA CORREGIDOS
        self.nombres_mapa = {
            "Barranca_del_Muerto_L7": "Barranca del M.",
            "Mixcoac_L7": "Mixcoac",
            "San_Antonio_L7": "San Antonio",        
            "San_Pedro_de_los_Pinos_L7": "San Pedro", 
            "Tacubaya_L7": "Tacubaya",
            "Constituyentes_L7": "Constituyentes",
            "Auditorio_L7": "Auditorio",
            "Polanco_L7": "Polanco",
            "Observatorio_L1": "Observatorio",
            "Tacubaya_L1": "Tacubaya",
            "Juanacatlan_L1": "Juanacatlán",
            "Chapultepec_L1": "Chapultepec",
            "Sevilla_L1": "Sevilla",
            "Insurgentes_L1": "Insurgentes",
            "Cuauhtemoc_L1": "Cuauhtémoc",
            "Balderas_L1": "Balderas",
            "Tacubaya_L9": "Tacubaya",
            "Patriotismo_L9": "Patriotismo",
            "Chilpancingo_L9": "Chilpancingo",
            "Centro_Medico_L9": "Centro Médico",
            "Lazaro_Cardenas_L9": "Lázaro Cárdenas", 
            "Universidad_L3": "Universidad",
            "Copilco_L3": "Copilco",
            "Miguel_Angel_de_Quevedo_L3": "M.A. Quevedo", 
            "Viveros_L3": "Viveros",
            "Coyoacan_L3": "Coyoacán",
            "Zapata_L3": "Zapata",
            "Division_del_Norte_L3": "División del N.", 
            "Eugenia_L3": "Eugenia",
            "Etiopia_L3": "Etiopía",
            "Centro_Medico_L3": "Centro Médico",
            "Hospital_General_L3": "Hosp. General",     
            "Ninos_Heroes_L3": "Niños Héroes",          
            "Balderas_L3": "Balderas",
            "Juarez_L3": "Juárez",
            "Mixcoac_L12": "Mixcoac",
            "Insurgentes_Sur_L12": "Insurgentes Sur",
            "Hospital_20_de_Noviembre_L12": "20 de Nov.", 
            "Zapata_L12": "Zapata",
            "Parque_de_los_Venados_L12": "P. de los Venados", 
            "Eje_Central_L12": "Eje Central" 
        }

        # NOMBRES BUSCADOR (Usamos los nombres bonitos)
        self.mapa_nombres_reales = {} 
        for nodo in self.mapa_logico.get_grafo().nodes():
            nombre_bonito = self.nombres_mapa.get(nodo, nodo.split('_')[0])
            if nombre_bonito not in self.mapa_nombres_reales:
                self.mapa_nombres_reales[nombre_bonito] = []
            self.mapa_nombres_reales[nombre_bonito].append(nodo)
        
        self.lista_estaciones = sorted(list(self.mapa_nombres_reales.keys()))

        # Datos Referencia
        self.terminales = {
            "L1": {"izq": "Observatorio", "der": "Pantitlán"},
            "L3": {"arriba": "Indios Verdes", "abajo": "Universidad"},
            "L7": {"arriba": "El Rosario", "abajo": "Barranca del Muerto"},
            "L9": {"izq": "Tacubaya", "der": "Pantitlán"},
            "L12": {"izq": "Mixcoac", "der": "Tláhuac"}
        }

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

        self.coords_gui = {
            # L7
            "Barranca_del_Muerto_L7": (150, 720), "Mixcoac_L7": (150, 620),
            "San_Antonio_L7": (150, 540), "San_Pedro_de_los_Pinos_L7": (150, 460),
            "Tacubaya_L7": (150, 380), "Constituyentes_L7": (150, 280),
            "Auditorio_L7": (150, 200), "Polanco_L7": (150, 120),
            # L1
            "Observatorio_L1": (60, 440), "Tacubaya_L1": (150, 380),      
            "Juanacatlan_L1": (230, 320), "Chapultepec_L1": (300, 280),
            "Sevilla_L1": (380, 280), "Insurgentes_L1": (460, 280),
            "Cuauhtemoc_L1": (540, 280), "Balderas_L1": (620, 280),      
            # L9
            "Tacubaya_L9": (150, 380), "Patriotismo_L9": (260, 380),
            "Chilpancingo_L9": (370, 380), "Centro_Medico_L9": (500, 380), 
            "Lazaro_Cardenas_L9": (620, 380),
            # L3
            "Universidad_L3": (500, 750), "Copilco_L3": (500, 700),
            "Miguel_Angel_de_Quevedo_L3": (500, 650), "Viveros_L3": (500, 600),
            "Coyoacan_L3": (500, 550), "Zapata_L3": (500, 500),        
            "Division_del_Norte_L3": (500, 450), "Eugenia_L3": (500, 415),
            "Etiopia_L3": (500, 400), "Centro_Medico_L3": (500, 380), 
            "Hospital_General_L3": (500, 330), "Ninos_Heroes_L3": (560, 305),  
            "Balderas_L3": (620, 280), "Juarez_L3": (620, 200),
            # L12
            "Mixcoac_L12": (150, 620), "Insurgentes_Sur_L12": (260, 620),
            "Hospital_20_de_Noviembre_L12": (370, 620), "Zapata_L12": (500, 500),       
            "Parque_de_los_Venados_L12": (600, 540), "Eje_Central_L12": (680, 540),
        }

        self.crear_layout()
        self.aplicar_tema()

    def crear_layout(self):
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_container, width=400, padx=30, pady=30)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.lbl_logo = tk.Label(self.sidebar, text="CDMX Metro", font=("Segoe UI Variable Display", 28, "bold"), anchor="w")
        self.lbl_logo.pack(fill=tk.X)
        self.lbl_sublogo = tk.Label(self.sidebar, text="Planificador Inteligente", font=("Segoe UI", 11), anchor="w")
        self.lbl_sublogo.pack(fill=tk.X, pady=(0, 40))

        self.crear_autocomplete("Punto de Partida", "origen")
        tk.Frame(self.sidebar, height=20, bg=self.sidebar['bg']).pack()
        self.crear_autocomplete("Destino Final", "destino")

        tk.Frame(self.sidebar, height=30, bg=self.sidebar['bg']).pack()
        
        # Checkbox Hora Punta
        self.chk_hora_punta = tk.Checkbutton(self.sidebar, text=" Hora Punta ⚠️", 
                                             variable=self.hora_punta_var,
                                             relief="flat", cursor="hand2", 
                                             font=("Segoe UI", 10, "bold"),
                                             highlightthickness=0, borderwidth=0,
                                             activebackground=self.sidebar['bg'],
                                             activeforeground="#EF4444")
        self.chk_hora_punta.pack(anchor="w", pady=(0, 10))

        self.btn_calc = BotonModerno(self.sidebar, "Calcular Ruta Óptima", self.calcular_ruta, width=340, height=55)
        self.btn_calc.pack()

        tk.Frame(self.sidebar, height=30, bg=self.sidebar['bg']).pack()
        self.lbl_res_titulo = tk.Label(self.sidebar, text="Detalles del viaje", font=("Segoe UI", 12, "bold"), anchor="w")
        self.lbl_res_titulo.pack(fill=tk.X, pady=(0, 10))

        self.txt_pasos = tk.Text(self.sidebar, height=15, font=("Segoe UI", 10), 
                                 relief="flat", wrap="word", padx=15, pady=15, 
                                 highlightthickness=0, state="disabled")
        self.txt_pasos.pack(fill=tk.BOTH, expand=True)
        self.configurar_tags_texto()

        self.btn_tema = tk.Button(self.sidebar, text="Cambiar Tema 🌓", command=self.cambiar_tema, 
                                  relief="flat", cursor="hand2", font=("Segoe UI", 10))
        self.btn_tema.pack(side=tk.BOTTOM, anchor="w")

        self.map_frame = tk.Frame(self.main_container)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.map_frame, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def crear_autocomplete(self, titulo, var_name):
        lbl = tk.Label(self.sidebar, text=titulo, font=("Segoe UI", 10, "bold"), anchor="w")
        lbl.pack(fill=tk.X, pady=(0, 8))
        if var_name == "origen": self.lbl_origen = lbl
        else: self.lbl_destino = lbl

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
        self.txt_pasos.tag_config("alerta", foreground="#EF4444", font=("Segoe UI", 10, "italic"))

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
        
        # Configurar Checkbox
        self.chk_hora_punta.config(bg=t["bg_panel"], fg=t["text_primary"], 
                                   selectcolor=t["bg_panel"], activebackground=t["bg_panel"])

        # ESTILO COMBOBOX
        bg_input = "#334155" if self.modo_oscuro else "#F9FAFB"
        fg_input = "white" if self.modo_oscuro else "#111827"
        
        self.style.map('TCombobox', 
                      fieldbackground=[('readonly', bg_input), ('!readonly', bg_input)],
                      background=[('readonly', bg_input)],
                      foreground=[('readonly', fg_input), ('!readonly', fg_input)],
                      selectbackground=[('readonly', bg_input)],
                      arrowcolor=[('readonly', fg_input)])
        
        btn_bg = "#818CF8" if self.modo_oscuro else "#4F46E5"
        btn_hover = "#6366F1" if self.modo_oscuro else "#4338CA"
        self.btn_calc.update_colors(t["bg_panel"], btn_bg, btn_hover)

        self.dibujar_mapa()

    def dibujar_mapa(self):
        self.canvas.delete("all")
        t = self.colores["oscuro"] if self.modo_oscuro else self.colores["claro"]
        grafo = self.mapa_logico.get_grafo()

        for u, v in grafo.edges():
            if u in self.coords_gui and v in self.coords_gui:
                x1, y1 = self.coords_gui[u]
                x2, y2 = self.coords_gui[v]
                linea_u = u.split('_')[-1]
                linea_v = v.split('_')[-1]
                
                if linea_u == linea_v:
                    color = self.lineas_color.get(linea_u, "#999")
                    w = 6
                else:
                    color = t["line_inactive"]
                    w = 3
                
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=w, capstyle=tk.ROUND, tags="mapa")

        r = 7
        for nodo in grafo.nodes():
            if nodo in self.coords_gui:
                x, y = self.coords_gui[nodo]
                nombre_mostrar = self.nombres_mapa.get(nodo, nodo.split('_')[0])
                linea = nodo.split('_')[-1]

                offset_x = 18
                offset_y = -5
                anchor_pos = "w"
                if "L7" in linea and "Tacubaya" not in nombre_mostrar and "Mixcoac" not in nombre_mostrar:
                    offset_x = -18
                    anchor_pos = "e"
                if "Juárez" in nombre_mostrar: offset_y = -15; offset_x = 0

                self.canvas.create_oval(x-(r+2), y-(r+2), x+(r+2), y+(r+2), fill=t["map_bg"], outline="", tags="mapa")
                item_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=t["node_fill"], outline=t["node_outline"], width=1.5, tags=("nodo", nodo))
                
                text_x = x + offset_x
                text_y = y + offset_y
                self.canvas.create_text(text_x, text_y, text=nombre_mostrar, anchor=anchor_pos, font=("Segoe UI", 8, "bold"), fill=t["map_bg"], width=150, angle=20)
                self.canvas.create_text(text_x, text_y, text=nombre_mostrar, anchor=anchor_pos, font=("Segoe UI", 8, "bold"), fill=t["text_map"], tags=("texto", nodo), angle=20)

                self.canvas.tag_bind(item_id, "<Enter>", lambda e, n=nodo, i=item_id: self.on_hover_enter(e, n, i))
                self.canvas.tag_bind(item_id, "<Leave>", lambda e, i=item_id: self.on_hover_leave(e, i))

    def on_hover_enter(self, event, nodo_id, item_id):
        self.canvas.itemconfig(item_id, width=3, outline=self.colores["oscuro" if self.modo_oscuro else "claro"]["text_primary"])
        nombre = self.nombres_mapa.get(nodo_id, nodo_id.split('_')[0])
        linea = nodo_id.split('_')[-1]
        info = f"{nombre}\n{self.info_lineas.get(linea, linea)}"
        self.tooltip = ToolTip(self.canvas)
        self.tooltip.showtip(info)

    def on_hover_leave(self, event, item_id):
        t = self.colores["oscuro"] if self.modo_oscuro else self.colores["claro"]
        self.canvas.itemconfig(item_id, width=1.5, outline=t["node_outline"])
        if hasattr(self, 'tooltip'): self.tooltip.hidetip()

    def get_direccion_linea(self, u, v, linea):
        if u not in self.coords_gui or v not in self.coords_gui: return ""
        if linea not in self.terminales: return ""
        xu, yu = self.coords_gui[u]
        xv, yv = self.coords_gui[v]
        dx = xv - xu
        dy = yv - yu
        terms = self.terminales[linea]
        if linea in ["L1", "L9", "L12"]: return terms["der"] if dx > 0 else terms["izq"]
        elif linea in ["L3", "L7"]: return terms["abajo"] if dy > 0 else terms["arriba"]
        return ""

    def obtener_mejor_nodo(self, nombre_origen, nombre_destino):
        candidatos_origen = self.mapa_nombres_reales.get(nombre_origen)
        candidatos_destino = self.mapa_nombres_reales.get(nombre_destino)
        if not candidatos_origen or not candidatos_destino: return None, None
        for u in candidatos_origen:
            linea_u = u.split('_')[-1]
            for v in candidatos_destino:
                linea_v = v.split('_')[-1]
                if linea_u == linea_v: return u, v
        return candidatos_origen[0], candidatos_destino[0]

    def calcular_ruta(self):
        origen_nombre = self.combo_origen.get()
        destino_nombre = self.combo_destino.get()

        if not origen_nombre or not destino_nombre:
            messagebox.showinfo("Ups", "Selecciona origen y destino.")
            return

        id_origen, id_destino = self.obtener_mejor_nodo(origen_nombre, destino_nombre)
        
        if not id_origen or not id_destino:
            messagebox.showerror("Error", "Estación no válida (Usa el autocompletado).")
            return

        ruta, costo_metros = self.buscador.encontrar_ruta(id_origen, id_destino)
        self.dibujar_mapa()
        
        if not ruta:
            self.mostrar_info("No se encontró ruta.")
            return

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
        
        if self.hora_punta_var.get():
            tiempo_viaje *= 1.5 
            
        tiempo_viaje = int(math.ceil(tiempo_viaje))

        self.mostrar_pasos_detallados(ruta, costo_metros, tiempo_viaje)
        self.animar_ruta(ruta, 0)

    def mostrar_pasos_detallados(self, ruta, distancia, tiempo):
        self.txt_pasos.config(state="normal")
        self.txt_pasos.delete(1.0, tk.END)
        self.txt_pasos.insert(tk.END, f"⏱ {tiempo} min total  |  📏 {int(distancia)} m\n\n", "titulo")
        
        if self.hora_punta_var.get():
            self.txt_pasos.insert(tk.END, "⚠ Retrasos por hora punta incluidos\n\n", "alerta")

        nodo_inicio = ruta[0]
        nombre_inicio = self.nombres_mapa.get(nodo_inicio, nodo_inicio.split('_')[0])
        linea_actual = nodo_inicio.split('_')[-1]
        
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
            
            if linea != linea_actual:
                if count > 0: self.txt_pasos.insert(tk.END, f"   ↓  {count} estaciones\n", "meta")
                nombre_trans = self.nombres_mapa.get(nodo, nodo.split('_')[0])
                if i == 1 and nombre_trans == nombre_inicio:
                    linea_actual = linea
                    if i+1 < len(ruta):
                        dir_term = self.get_direccion_linea(ruta[i], ruta[i+1], linea)
                        if dir_term: 
                             self.txt_pasos.insert(tk.END, f"   → Cambio a {self.info_lineas.get(linea)} (Dir. {dir_term})\n", "direccion")
                    continue
                self.txt_pasos.insert(tk.END, f"• TRANSBORDO en {nombre_trans}\n", "transbordo")
                if i+1 < len(ruta):
                    dir_term = self.get_direccion_linea(ruta[i], ruta[i+1], linea)
                    if dir_term:
                        self.txt_pasos.insert(tk.END, f"   → {self.info_lineas.get(linea)} (Dir. {dir_term})\n", "direccion")
                linea_actual = linea
                count = 0
            else:
                count += 1
        
        if count > 0: self.txt_pasos.insert(tk.END, f"   ↓  {count} estaciones\n", "meta")
        nombre_fin = self.nombres_mapa.get(ruta[-1], ruta[-1].split('_')[0])
        self.txt_pasos.insert(tk.END, f"🏁 Llegada a {nombre_fin}", "titulo")
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