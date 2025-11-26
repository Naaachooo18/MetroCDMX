import networkx as nx
from math import radians, cos, sin, asin, sqrt

class AEstrella:
    def __init__(self, mapa_objeto):
        """
        :param mapa_objeto: Instancia de la clase Mapa ya inicializada.
        """
        self.mapa = mapa_objeto.get_grafo()
        self.posiciones = mapa_objeto.get_posiciones()

    def heuristica_haversine(self, nodo_actual, nodo_destino):
        """
        Calcula la distancia Haversine (distancia en esfera) entre dos puntos
        geográficos. Esta es la función h(n).
        """
        # Obtener coordenadas (lat, lon)
        try:
            lat1, lon1 = self.posiciones[nodo_actual]
            lat2, lon2 = self.posiciones[nodo_destino]
        except KeyError:
            # Si un nodo no tiene coordenadas (por seguridad), retornamos 0
            return 0

        # Convertir grados a radianes
        lat1, lon1 = map(radians, (lat1, lon1))
        lat2, lon2 = map(radians, (lat2, lon2))

        # Fórmula de Haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6371000  # Radio de la Tierra en metros
        
        distancia_recta = c * r
        return distancia_recta

    def encontrar_ruta(self, estacion_origen_id, estacion_destino_id):
        """
        Ejecuta A* usando networkx y la heurística personalizada.
        """
        try:
            print(f"Calculando ruta A* de {estacion_origen_id} a {estacion_destino_id}...")
            
            ruta = nx.astar_path(
                self.mapa,
                source=estacion_origen_id,
                target=estacion_destino_id,
                heuristic=self.heuristica_haversine,
                weight="weight"
            )
            
            coste_total = nx.path_weight(self.mapa, ruta, weight="weight")
            return ruta, coste_total
            
        except nx.NetworkXNoPath:
            print("No se encontró ruta entre las estaciones seleccionadas.")
            return None, 0
        except Exception as e:
             print(f"Error en A*: {e}")
             return None, 0