import networkx as nx
import matplotlib.pyplot as plt
from Mapa import Mapa

# 1. Cargar tus datos
metro = Mapa()
G = metro.get_grafo()
pos_lat_lon = metro.get_posiciones()

# 2. Ajustar coordenadas (NetworkX quiere X,Y -> Longitud, Latitud)
# Tus datos están en (Lat, Lon), así que les damos la vuelta para el dibujo
pos_xy = {nodo: (coord[1], coord[0]) for nodo, coord in pos_lat_lon.items()}

# 3. DIBUJAR USANDO NETWORKX
plt.figure(figsize=(10, 8)) # Tamaño de ventana

# Esta es la función mágica que lo hace todo automático
nx.draw(G, 
        pos=pos_xy,           # Usar las coordenadas reales
        with_labels=True,     # Poner nombres
        node_size=50,         # Puntos pequeños
        node_color='red',     # Color nodos
        font_size=6,          # Letra pequeña para que quepa
        width=1.5)            # Grosor líneas

plt.title("Grafo Real (NetworkX + Geografía)")
plt.axis('equal') # Para que el mapa no salga estirado
plt.show()