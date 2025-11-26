import networkx as nx
import matplotlib.pyplot as plt
from Mapa import Mapa

#Carga los datos 
metro = Mapa()  
G = metro.get_grafo()
pos_lat_lon = metro.get_posiciones()

#Ajusta las coordenadas ya que la funcion usa  longitud,latitud en vez de latitud,longitud
pos_xy = {nodo: (coord[1], coord[0]) for nodo, coord in pos_lat_lon.items()}

# Dibuja usando networkx
plt.figure(figsize=(10, 8)) 

nx.draw(G, 
        pos=pos_xy,           # coordenadas
        with_labels=True,     # Pone los nombres
        node_size=50,         # Tamaño de los puntos
        node_color='red',     # Color del nodo
        font_size=6,          # Tamaño de la letra
        width=1.5)            # Grosor

plt.title("Grafo Real (NetworkX + Geografía)")
plt.axis('equal') # Para que el mapa salga centrado
plt.show()