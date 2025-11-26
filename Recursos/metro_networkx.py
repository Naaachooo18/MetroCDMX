import networkx as nx
import matplotlib.pyplot as plt

# Crear grafo
G = nx.Graph()

# Añadir nodos (estaciones)
G.add_node("Observatorio")
G.add_node("Tacubaya")
G.add_node("Juanacatlán")

# Añadir aristas (conexiones con peso)
G.add_edge("Observatorio", "Tacubaya", weight=1)
G.add_edge("Tacubaya", "Juanacatlán", weight=1)

# Dibujar el grafo (opcional)
nx.draw(G, with_labels=True, node_color="lightblue", font_weight="bold")
plt.show()

# Usar el algoritmo A*
path = nx.astar_path(G, "Observatorio", "Juanacatlán", heuristic=lambda u, v: 0, weight="weight")
print("Ruta óptima:", path)

# Coste total
cost = nx.path_weight(G, path, weight="weight")
print("Coste total:", cost)
