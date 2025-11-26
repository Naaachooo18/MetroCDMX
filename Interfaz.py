import tkinter as tk
from tkinter import ttk, messagebox
import math
import unicodedata

from Mapa import Mapa
from AEstrella import AEstrella
    
class Placements:# coordenadas base
    BASE_WIDTH = 800
    BASE_HEIGHT = 800

    COORDS_GUI = { #establecemos las coordenadas de cada estación
        # L7 (Naranja)
        "Barranca_del_Muerto_L7": (150, 720), "Mixcoac_L7": (150, 620),
        "San_Antonio_L7": (150, 540), "San_Pedro_de_los_Pinos_L7": (150, 460),
        "Tacubaya_L7": (150, 380), "Constituyentes_L7": (150, 280),
        "Auditorio_L7": (150, 200), "Polanco_L7": (150, 120),
        # L1 (Rosa)
        "Observatorio_L1": (60, 440), "Tacubaya_L1": (150, 380),      
        "Juanacatlan_L1": (230, 320), "Chapultepec_L1": (300, 280),
        "Sevilla_L1": (380, 280), "Insurgentes_L1": (460, 280),
        "Cuauhtemoc_L1": (530, 280), "Balderas_L1": (600, 280),      
        # L9 (Marrón)
        "Tacubaya_L9": (150, 380), "Patriotismo_L9": (260, 380),
        "Chilpancingo_L9": (370, 380), "Centro_Medico_L9": (500, 380), 
        "Lazaro_Cardenas_L9": (620, 380),
        # L3 (Verde)
        "Universidad_L3": (500, 750), "Copilco_L3": (500, 700),
        "Miguel_Angel_de_Quevedo_L3": (500, 650), "Viveros_L3": (500, 600),
        "Coyoacan_L3": (500, 550), "Zapata_L3": (500, 500),        
        "Division_del_Norte_L3": (500, 450), "Eugenia_L3": (500, 415),
        "Etiopia_L3": (500, 400), "Centro_Medico_L3": (500, 380), 
        "Hospital_General_L3": (500, 330), "Ninos_Heroes_L3": (550, 320),  
        "Balderas_L3": (600, 280), "Juarez_L3": (600, 200),
        # L12 (Dorada)
        "Mixcoac_L12": (150, 620), "Insurgentes_Sur_L12": (260, 620),
        "Hospital_20_de_Noviembre_L12": (370, 620), "Zapata_L12": (500, 500),       
        "Parque_de_los_Venados_L12": (600, 540), "Eje_Central_L12": (680, 540),
    }
    #angulos base de las lineas
    LINE_DEFAULT_ANGLES = {"L1": 0, "L3": 0, "L7": 0, "L9": 0, "L12": 0}
    #posición de los nombres
    TEXT_PLACEMENTS = {
        "Barranca del M.": (-18, 0, "e", None), "San Antonio": (-18, 0, "e", None),
        "Constituyentes": (-18, 0, "e", None), "Auditorio": (-18, 0, "e", None), "Polanco": (-18, 0, "e", None),
        "San Pedro": (18, 0, "w", None), 
        "Observatorio": (20, 20, "s", 0), "Juanacatlán": (0, -18, "s", 0),   
        "Chapultepec": (0, -18, "s", 0), "Sevilla": (0, -18, "s", 0),     
        "Insurgentes": (0, 18, "n", 0), "Cuauhtémoc": (0, -18, "s", 0),  
        "Patriotismo": (0, 18, "n", 0), "Chilpancingo": (0, 18, "n", 0), 
        "Lázaro Cárdenas": (0, 18, "n", 0), 
        "Universidad": (18, 0, "w", 0), "Copilco": (18, 0, "w", 0),
        "M.A. Quevedo": (18, 0, "w", 0), "Viveros": (18, 0, "w", 0),
        "Coyoacán": (18, 0, "w", 0), "División del N.": (-18, 0, "e", 0),
        "Eugenia": (-18, 0, "e", 0), "Etiopía": (-18, 0, "e", 0), 
        "Hosp. General": (-18, 0, "e", 0), "Niños Héroes": (18, 0, "w", 0),  
        "Juárez": (0, -18, "s", 0), "Insurgentes Sur": (0, 18, "n", 0), 
        "20 de Nov.": (0, 18, "n", 0), "P. de los Venados": (0, 18, "n", 0), 
        "Eje Central": (0, -25, "n", 0),      
        "Mixcoac": (-18, 0, "e", 0), "Balderas": (18, 0, "w", 0),           
        "Tacubaya": (-18, 0, "e", 0), "Zapata": (-18, 0, "e", 0),            
        "Centro Médico": (47, -10, "s", 0),      
    }
    #posición base
    DEFAULT_PLACEMENT = (18, 0, "w", 0) 

#creamos un tooltip para poder pasar el ratón por un nodo y que nos muestre información
class ToolTip:
    # Constructor de la clase
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
    # Calcula la posición del cursor despliega una ventana flotante sin bordes
    def showtip(self, text):
        if self.tipwindow or not text: return
        x = self.widget.winfo_pointerx() + 15
        y = self.widget.winfo_pointery() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, justify=tk.LEFT, background="#1F2937", fg="#F3F4F6", relief=tk.SOLID, borderwidth=0, font=("Segoe UI", 9), padx=8, pady=4)
        label.pack()
    # Cierra y destruye la ventana del tooltip si está visible
    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

# --- BUSCADOR INTELIGENTE ---
class BuscadorInteligente(tk.Frame):
    # Inicializa el widget, configura el campo de entrada y vincula los eventos de teclado y foco
    def __init__(self, parent, lista_completa, font=("Segoe UI", 11), **kwargs):
        super().__init__(parent, **kwargs)
        self.lista_completa = lista_completa
        self.var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.var, font=font, relief="flat", bg="#334155", fg="white", insertbackground="white")
        self.entry.pack(fill=tk.X, ipady=8, padx=10)
        self.entry.bind('<KeyRelease>', self.on_keyrelease)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<Down>', self.mover_abajo)
        self.entry.bind('<Up>', self.mover_arriba)
        self.entry.bind('<Return>', self.seleccionar_tecla)
        self.listbox_window = None
    # Elimina acentos y convierte a minúsculas para facilitar la búsqueda
    def _normalizar(self, texto: str) -> str:
        if texto is None: return ""
        nf = unicodedata.normalize('NFD', texto)
        return ''.join(ch for ch in nf if unicodedata.category(ch) != 'Mn').lower()
    # Filtra la lista de opciones basándose en el texto escrito por el usuario.
    def on_keyrelease(self, event):
        if event.keysym in ('Up', 'Down', 'Return', 'Tab', 'Left', 'Right'): return
        valor = self.var.get()
        if valor == '': self.ocultar_lista()
        else:
            valor_norm = self._normalizar(valor)
            filtrada = [item for item in self.lista_completa if valor_norm in self._normalizar(item)]
            self.mostrar_lista(filtrada)
    # Muestra o actualiza la ventana flotante con las sugerencias filtradas debajo
    def mostrar_lista(self, items):
        if not items:
            self.ocultar_lista()
            return
        if not self.listbox_window:
            self.listbox_window = tk.Toplevel(self)
            self.listbox_window.wm_overrideredirect(True)
            self.listbox_window.wm_attributes("-topmost", True)
            self.listbox = tk.Listbox(self.listbox_window, font=("Segoe UI", 10), bg="#1E293B", fg="white", selectbackground="#2563EB", relief="flat", borderwidth=0, height=5)
            self.listbox.pack(fill=tk.BOTH, expand=True)
            self.listbox.bind('<<ListboxSelect>>', self.on_select_click)

        self.listbox.delete(0, tk.END)
        for item in items: self.listbox.insert(tk.END, item)

        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        w = self.entry.winfo_width()
        self.listbox_window.wm_geometry(f"{w}x{150}+{x}+{y}")
    # Cierra la ventana de sugerencias si está abierta
    def ocultar_lista(self):
        if self.listbox_window:
            self.listbox_window.destroy()
            self.listbox_window = None
    # Maneja la selección de un elemento mediante clic del ratón
    def on_select_click(self, event):
        if not self.listbox.curselection(): return
        self.set_value(self.listbox.get(self.listbox.curselection()[0]))
    # Maneja la selección de un elemento mediante la tecla Enter
    def seleccionar_tecla(self, event):
        if self.listbox_window and self.listbox.curselection():
            self.set_value(self.listbox.get(self.listbox.curselection()[0]))
    # Establece el valor seleccionado en el campo de entrada y cierra la lista
    def set_value(self, valor):
        self.var.set(valor)
        self.entry.icursor(tk.END)
        self.ocultar_lista()
    # Retorna el texto actual del campo de entrada
    def get(self):
        return self.var.get()
    # Transfieren el foco a la lista para permitir la navegación con las flechas
    def mover_abajo(self, event):
        if self.listbox_window:
            self.listbox.focus_set()
            self.listbox.selection_set(0)

    def mover_arriba(self, event):
        if self.listbox_window:
            self.listbox.focus_set()
            self.listbox.selection_set(0)
    # Gestionan el cierre de la lista cuando el usuario hace clic fuera del widget
    def on_focus_out(self, event):
        self.after(200, self.check_focus)

    def check_focus(self):
        try:
            focus = self.focus_get()
            if focus != self.listbox and focus != self.entry: self.ocultar_lista()
        except: pass
    # Actualiza la configuración de colores del widget
    def actualizar_colores(self, bg_input, fg_input, bg_panel=None):
        self.entry.config(bg=bg_input, fg=fg_input, insertbackground=fg_input)
        if bg_panel: self.config(bg=bg_panel)
        if self.listbox_window: self.listbox.config(bg="#1E293B", fg="white")

# --- CLASE BOTÓN MODERNO ---
class BotonModerno(tk.Canvas):
    # Inicializa el lienzo, dibuja la forma redondeada y el texto, y vincula los eventos del ratón
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
    # Dibuja un polígono que simula un rectángulo con esquinas redondeadas
    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.create_polygon(points, **kwargs, smooth=True)
    # Cambia el color y el ratón cuando entra en el botón (hover)
    def on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")
    # Restaura el ratón y el color del botón
    def on_leave(self, e):
        self.itemconfig(self.rect, fill=self.bg_color)
    # Ejecuta la función asignada cuando se hace clic en el botón
    def on_click(self, e):
        if self.command: self.command()
    # Actualiza los colores del botón y del fondo
    def update_colors(self, parent_bg, btn_bg, btn_hover):
        self.config(bg=parent_bg)
        self.bg_color = btn_bg
        self.hover_color = btn_hover
        self.itemconfig(self.rect, fill=btn_bg)

# --- INTERFAZ PRINCIPAL ---
class InterfazMetro2025:
    # Inicializa la ventana, carga la lógica del mapa y prepara los diccionarios y estilos visuales
    def __init__(self, root):
        self.root = root
        self.root.title("Metro CDMX • Navigator 2025")
        self.root.geometry("1280x850")
        
        self.style = ttk.Style()
        self.style.theme_use('clam') 
        
        self.mapa_logico = Mapa()
        self.buscador = AEstrella(self.mapa_logico)
        
        self.hora_punta_var = tk.BooleanVar()
        self.hora_punta_var.set(False)

        self.colores = {
            "bg_app": "#0F172A", "bg_panel": "#1E293B", "text_primary": "#F8FAFC", "text_secondary": "#94A3B8", 
            "map_bg": "#0F172A", "line_inactive": "#334155", "node_fill": "#1E293B", "node_outline": "#94A3B8", "text_map": "#CBD5E1"
        }
        self.lineas_color = { "L1": "#EC4899", "L3": "#84CC16", "L7": "#F97316", "L9": "#A97142", "L12": "#EAB308" }
        self.info_lineas = { "L1": "Línea 1", "L3": "Línea 3", "L7": "Línea 7", "L9": "Línea 9", "L12": "Línea 12" }

        self.nombres_mapa = {
            "Barranca_del_Muerto_L7": "Barranca del M.", "Mixcoac_L7": "Mixcoac",
            "San_Antonio_L7": "San Antonio", "San_Pedro_de_los_Pinos_L7": "San Pedro", 
            "Tacubaya_L7": "Tacubaya", "Constituyentes_L7": "Constituyentes",
            "Auditorio_L7": "Auditorio", "Polanco_L7": "Polanco",
            "Observatorio_L1": "Observatorio", "Tacubaya_L1": "Tacubaya",
            "Juanacatlan_L1": "Juanacatlán", "Chapultepec_L1": "Chapultepec",
            "Sevilla_L1": "Sevilla", "Insurgentes_L1": "Insurgentes",
            "Cuauhtemoc_L1": "Cuauhtémoc", "Balderas_L1": "Balderas",
            "Tacubaya_L9": "Tacubaya", "Patriotismo_L9": "Patriotismo",
            "Chilpancingo_L9": "Chilpancingo", "Centro_Medico_L9": "Centro Médico",
            "Lazaro_Cardenas_L9": "Lázaro Cárdenas", "Universidad_L3": "Universidad", 
            "Copilco_L3": "Copilco", "Miguel_Angel_de_Quevedo_L3": "M.A. Quevedo", 
            "Viveros_L3": "Viveros", "Coyoacan_L3": "Coyoacán", "Zapata_L3": "Zapata",
            "Division_del_Norte_L3": "División del N.", "Eugenia_L3": "Eugenia",
            "Etiopia_L3": "Etiopía", "Centro_Medico_L3": "Centro Médico",
            "Hospital_General_L3": "Hosp. General", "Ninos_Heroes_L3": "Niños Héroes",          
            "Balderas_L3": "Balderas", "Juarez_L3": "Juárez",
            "Mixcoac_L12": "Mixcoac", "Insurgentes_Sur_L12": "Insurgentes Sur",
            "Hospital_20_de_Noviembre_L12": "20 de Nov.", "Zapata_L12": "Zapata",
            "Parque_de_los_Venados_L12": "P. de los Venados", "Eje_Central_L12": "Eje Central" 
        }

        self.mapa_nombres_reales = {} 
        for nodo in self.mapa_logico.get_grafo().nodes():
            nombre_bonito = self.nombres_mapa.get(nodo, nodo.split('_')[0])
            if nombre_bonito not in self.mapa_nombres_reales:
                self.mapa_nombres_reales[nombre_bonito] = []
            self.mapa_nombres_reales[nombre_bonito].append(nodo)
        self.lista_estaciones = sorted(list(self.mapa_nombres_reales.keys()))

        self.terminales = {
            "L1": {"izq": "Observatorio", "der": "Balderas"}, "L3": {"arriba": "Juárez", "abajo": "Universidad"},
            "L7": {"arriba": "Polanco", "abajo": "Barranca del Muerto"}, "L9": {"izq": "Tacubaya", "der": "Lázaro Cárdenas"},
            "L12": {"izq": "Mixcoac", "der": "Eje Central"}
        }

        self.crear_layout()
        self.aplicar_tema_fijo()
    # Divide la ventana en panel lateral con los conotroles y el mapa
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

        self.crear_buscador("Punto de Partida", "origen")
        self.crear_buscador("Destino Final", "destino", padding=(20, 0))

        self.chk_hora_punta = tk.Checkbutton(self.sidebar, text=" Hora Punta ⚠️", variable=self.hora_punta_var,
                                             relief="flat", cursor="hand2", font=("Segoe UI", 10, "bold"),
                                             highlightthickness=0, borderwidth=0, activebackground=self.sidebar['bg'], activeforeground="#EF4444")
        self.chk_hora_punta.pack(anchor="w", pady=(30, 10))

        self.btn_calc = BotonModerno(self.sidebar, "Calcular Ruta Óptima", self.calcular_ruta, width=340, height=55)
        self.btn_calc.pack(pady=(0, 30))

        self.lbl_res_titulo = tk.Label(self.sidebar, text="Detalles del viaje", font=("Segoe UI", 12, "bold"), anchor="w")
        self.lbl_res_titulo.pack(fill=tk.X, pady=(0, 10))

        self.txt_pasos = tk.Text(self.sidebar, height=15, font=("Segoe UI", 10), relief="flat", wrap="word", padx=15, pady=15, highlightthickness=0, state="disabled")
        self.txt_pasos.pack(fill=tk.BOTH, expand=True)
        self.configurar_tags_texto()

        self.map_frame = tk.Frame(self.main_container)
        self.map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.map_frame, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.redimensionar_mapa)
    # Método auxiliar para instanciar los widgets de la búsqueda y evitar la duplicidad del código
    def crear_buscador(self, titulo, var_name, padding=(0, 0)):
        lbl = tk.Label(self.sidebar, text=titulo, font=("Segoe UI", 10, "bold"), anchor="w")
        lbl.pack(fill=tk.X, pady=(padding[0], 8)) 
        if var_name == "origen": self.lbl_origen = lbl
        else: self.lbl_destino = lbl

        cb = BuscadorInteligente(self.sidebar, self.lista_estaciones, bg="#1E293B")
        cb.pack(fill=tk.X, pady=(0, padding[1])) 
        if var_name == "origen": self.combo_origen = cb
        else: self.combo_destino = cb
    # Define los estilos de formato para el texto de la ruta
    def configurar_tags_texto(self):
        self.txt_pasos.tag_config("titulo", font=("Segoe UI", 11, "bold"))
        self.txt_pasos.tag_config("meta", foreground="#888")
        self.txt_pasos.tag_config("direccion", foreground="#2563EB", font=("Segoe UI", 10, "bold"))
        self.txt_pasos.tag_config("transbordo", foreground="#EF4444", font=("Segoe UI", 10, "bold"))
        self.txt_pasos.tag_config("pasos", lmargin1=15, lmargin2=15)
        self.txt_pasos.tag_config("alerta", foreground="#EF4444", font=("Segoe UI", 10, "italic"))
    # Aplica la misma paleta de colores a todos los elementos
    def aplicar_tema_fijo(self):
        t = self.colores
        self.root.config(bg=t["bg_app"])
        self.main_container.config(bg=t["bg_app"])
        self.sidebar.config(bg=t["bg_panel"])
        self.map_frame.config(bg=t["map_bg"])
        self.canvas.config(bg=t["map_bg"])
        
        for l in [self.lbl_logo, self.lbl_res_titulo]: l.config(bg=t["bg_panel"], fg=t["text_primary"])
        for l in [self.lbl_sublogo, self.lbl_origen, self.lbl_destino]: l.config(bg=t["bg_panel"], fg=t["text_secondary"])
        
        self.txt_pasos.config(bg=t["bg_app"], fg=t["text_primary"])
        self.chk_hora_punta.config(bg=t["bg_panel"], fg=t["text_primary"], selectcolor=t["bg_panel"], activebackground=t["bg_panel"])

        self.combo_origen.actualizar_colores("#334155", "white", t["bg_panel"])
        self.combo_destino.actualizar_colores("#334155", "white", t["bg_panel"])
        self.btn_calc.update_colors(t["bg_panel"], "#818CF8", "#6366F1")
        self.dibujar_mapa()
    # Cambia el tamaño del mapa cuando reajustas el tamaño de la ventana
    def redimensionar_mapa(self, event):
        self.dibujar_mapa()
    # Calcula la escala y el centrado para ajustar las coordenadas al tamaño actual del canvas
    def obtener_transformacion(self):
        w_actual = self.canvas.winfo_width()
        h_actual = self.canvas.winfo_height()
        if w_actual < 50 or h_actual < 50: return 1, 0, 0

        all_coords = list(Placements.COORDS_GUI.values())
        xs = [c[0] for c in all_coords]
        ys = [c[1] for c in all_coords]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        content_w = max_x - min_x
        content_h = max_y - min_y
        margin = 100
        
        scale_x = (w_actual - margin) / content_w
        scale_y = (h_actual - margin) / content_h
        scale = min(scale_x, scale_y)

        visual_w = content_w * scale
        visual_h = content_h * scale
        offset_x = (w_actual - visual_w) / 2
        offset_y = (h_actual - visual_h) / 2
        
        dx = offset_x - (min_x * scale)
        dy = offset_y - (min_y * scale)
        return scale, dx, dy
    #dibuja las nodos y las aristas en el canvas
    def dibujar_mapa(self):
        self.canvas.delete("all") #borra el dibujo anterior
        t = self.colores
        grafo = self.mapa_logico.get_grafo()
        scale, dx, dy = self.obtener_transformacion()
        drawn_names = set()
        #dibuja las aristas
        for u, v in grafo.edges():
            #solo dibuja si tienen coordenadas asignadas
            if u in Placements.COORDS_GUI and v in Placements.COORDS_GUI:
                x1_b, y1_b = Placements.COORDS_GUI[u]
                x2_b, y2_b = Placements.COORDS_GUI[v]
                x1 = x1_b * scale + dx
                y1 = y1_b * scale + dy
                x2 = x2_b * scale + dx
                y2 = y2_b * scale + dy

                linea_u = u.split('_')[-1]
                linea_v = v.split('_')[-1]
                #comprueba que las estaciones pertenezacan a la misma arista y pinta la linea
                if linea_u == linea_v:
                    color = self.lineas_color.get(linea_u, "#999")
                    w = 6 * scale
                else:
                    color = t["line_inactive"]
                    w = 3 * scale
                    #dibuja la linea en el canvas
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=w, capstyle=tk.ROUND, tags="mapa")
        #dibujo los nodos
        r = 7 * scale
        font_size = int(8 * scale)
        font_size = max(6, min(font_size, 12)) 

        for nodo in grafo.nodes():
            if nodo in Placements.COORDS_GUI:
                x_b, y_b = Placements.COORDS_GUI[nodo]
                x = x_b * scale + dx
                y = y_b * scale + dy
                #obtiene el nombre
                nombre = self.nombres_mapa.get(nodo, nodo.split('_')[0])
                linea = nodo.split('_')[-1]
                #dibuja el circulo exterior del nodo
                self.canvas.create_oval(x-(r+2), y-(r+2), x+(r+2), y+(r+2), fill=t["map_bg"], outline="", tags="mapa")
                #dibuja el interior del circulo
                item_id = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=t["node_fill"], outline=t["node_outline"], width=1.5*scale, tags=("nodo", nodo))
                
                #dibuja el nombre
                if nombre not in drawn_names:
                    #busca la posición del nombre
                    placement = Placements.TEXT_PLACEMENTS.get(nombre)
                    if placement:
                        off_x, off_y, anchor, ang = placement
                    else:
                        off_x, off_y, anchor, ang = Placements.DEFAULT_PLACEMENT
                    #si no tiene ángulo coge el mismo que la linea
                    if ang is None: ang = Placements.LINE_DEFAULT_ANGLES.get(linea, 0)
                    
                    #posición del nombre
                    t_x = x + (off_x * scale)
                    t_y = y + (off_y * scale)
                    
                    #ponemos negrita al nombre
                    self.canvas.create_text(t_x, t_y, text=nombre, anchor=anchor, font=("Segoe UI", font_size, "bold"), fill=t["map_bg"], width=150, angle=ang)
                    #texto real
                    self.canvas.create_text(t_x, t_y, text=nombre, anchor=anchor, font=("Segoe UI", font_size, "bold"), fill=t["text_map"], tags=("texto", nodo), angle=ang)
                    drawn_names.add(nombre)
                #muestra el tooltip cuando se pone el cursor sobre el nodo
                self.canvas.tag_bind(item_id, "<Enter>", lambda e, n=nodo, i=item_id: self.on_hover_enter(e, n, i))
                #oculta el tooltip cuando el cursor sale del nodo
                self.canvas.tag_bind(item_id, "<Leave>", lambda e, i=item_id: self.on_hover_leave(e, i))
    
    #resalta el nodo cuando el cursor está encima del nodo 
    def on_hover_enter(self, event, nodo_id, item_id):
        self.canvas.itemconfig(item_id, width=3, outline=self.colores["text_primary"])
        #obtiene el nombre de la estación
        nombre = self.nombres_mapa.get(nodo_id, nodo_id.split('_')[0])
        linea = nodo_id.split('_')[-1]
        #construye el texot que aparece en el tooltip(nombre de la estación y linea)
        info = f"{nombre}\n{self.info_lineas.get(linea, linea)}"
        #asocia el tooltip con el canvas
        self.tooltip = ToolTip(self.canvas)
        #muestra el tooltip 
        self.tooltip.showtip(info)
    
    #cuando el cursor abandona el nodo, este vuelve a su estado original
    def on_hover_leave(self, event, item_id):
        t = self.colores
        self.canvas.itemconfig(item_id, width=1.5, outline=t["node_outline"])
        #si el tooltip esta activado lo oculta
        if hasattr(self, 'tooltip'): self.tooltip.hidetip()


    def get_direccion_linea(self, u, v, linea):
        if u not in Placements.COORDS_GUI or v not in Placements.COORDS_GUI: return ""
        if linea not in self.terminales: return ""
        xu, yu = Placements.COORDS_GUI[u]
        xv, yv = Placements.COORDS_GUI[v]
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
            messagebox.showerror("Error", "Estación no válida.")
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
        if self.hora_punta_var.get(): tiempo_viaje *= 1.5
        tiempo_viaje = int(math.ceil(tiempo_viaje))

        self.mostrar_pasos_detallados(ruta, costo_metros, tiempo_viaje)
        self.animar_ruta(ruta, 0)

    def mostrar_pasos_detallados(self, ruta, distancia, tiempo):
        self.txt_pasos.config(state="normal")
        self.txt_pasos.delete(1.0, tk.END)
        self.txt_pasos.insert(tk.END, f"⏱ {tiempo} min total  |  📏 {int(distancia)} m\n\n", "titulo")
        if self.hora_punta_var.get(): self.txt_pasos.insert(tk.END, "⚠ Retrasos por hora punta incluidos\n\n", "alerta")

        nodo_inicio = ruta[0]
        nombre_inicio = self.nombres_mapa.get(nodo_inicio, nodo_inicio.split('_')[0])
        linea_actual = nodo_inicio.split('_')[-1]
        dir_str = ""
        if len(ruta) > 1:
            dir_term = self.get_direccion_linea(ruta[0], ruta[1], linea_actual)
            if dir_term: dir_str = f"Dir. {dir_term}"

        self.txt_pasos.insert(tk.END, f"• Inicio en {nombre_inicio}\n", "pasos")
        if dir_str: self.txt_pasos.insert(tk.END, f"   → {self.info_lineas.get(linea_actual)} ({dir_str})\n", "direccion")
        
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
                        if dir_term: self.txt_pasos.insert(tk.END, f"   → Cambio a {self.info_lineas.get(linea)} (Dir. {dir_term})\n", "direccion")
                    continue
                self.txt_pasos.insert(tk.END, f"• TRANSBORDO en {nombre_trans}\n", "transbordo")
                if i+1 < len(ruta):
                    dir_term = self.get_direccion_linea(ruta[i], ruta[i+1], linea)
                    if dir_term: self.txt_pasos.insert(tk.END, f"   → {self.info_lineas.get(linea)} (Dir. {dir_term})\n", "direccion")
                linea_actual = linea
                count = 0
            else: count += 1
        
        if count > 0: self.txt_pasos.insert(tk.END, f"   ↓  {count} estaciones\n", "meta")
        nombre_fin = self.nombres_mapa.get(ruta[-1], ruta[-1].split('_')[0])
        self.txt_pasos.insert(tk.END, f"🏁 Llegada a {nombre_fin}", "titulo")
        self.txt_pasos.config(state="disabled")

    def mostrar_info(self, texto):
        self.txt_pasos.config(state="normal")
        self.txt_pasos.delete(1.0, tk.END)
        self.txt_pasos.insert(tk.END, texto)
        self.txt_pasos.config(state="disabled")

    def resaltar_nodo(self, nodo, color, scale, dx, dy):
        if nodo in Placements.COORDS_GUI:
            x_base, y_base = Placements.COORDS_GUI[nodo]
            x = x_base * scale + dx
            y = y_base * scale + dy
            r = 9 * scale
            borde = "white"
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=borde, width=2, tags="ruta_animada")

    def animar_ruta(self, ruta, index):
        scale, dx, dy = self.obtener_transformacion()
        if index >= len(ruta) - 1: 
            self.resaltar_nodo(ruta[-1], "#EF4444", scale, dx, dy) 
            return

        u = ruta[index]
        v = ruta[index+1]
        nombre_u = u.rsplit('_', 1)[0]
        nombre_v = v.rsplit('_', 1)[0]
        
        if index == 0: self.resaltar_nodo(u, "#3B82F6", scale, dx, dy)
        elif nombre_u == nombre_v: self.resaltar_nodo(u, "#FACC15", scale, dx, dy)

        if u in Placements.COORDS_GUI and v in Placements.COORDS_GUI:
            x1_base, y1_base = Placements.COORDS_GUI[u]
            x2_base, y2_base = Placements.COORDS_GUI[v]
            x1 = x1_base * scale + dx
            y1 = y1_base * scale + dy
            x2 = x2_base * scale + dx
            y2 = y2_base * scale + dy
            color = "#22D3EE"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=5*scale, capstyle=tk.ROUND)
        
        self.root.after(150, lambda: self.animar_ruta(ruta, index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    app = InterfazMetro2025(root)
    root.mainloop()