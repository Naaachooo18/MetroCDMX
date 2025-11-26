import networkx as nx
from math import radians, cos, sin, asin, sqrt

class AEstrella:
    def __init__(self, mapa_objeto):
        # Constructor de la clase AEstrella:
        # Extraemos el grafo completo (nodos y aristas con sus pesos g(n)):
        self.mapa = mapa_objeto.get_grafo()
        # Extraemos las coordenadas de las (latitud, longitud):
        self.posiciones = mapa_objeto.get_posiciones()

    def heuristica_haversine(self, nodo_actual, nodo_destino):
        # Funcion heurística f(n)
        # Calcula la distancia en linea recta entre dos estaciones
        # Se utiliza la fomrula de Haversine ya que la tierra al ser redonda las 
        # distancia no se pueden calcular de manera lineas.


        # Intentar obtener las coordenadas de ambos nodos, self.posiciones es como un
        # diccionario, {"Observatorio": (19.3244, -99.1738)}
        try:
            lat1, lon1 = self.posiciones[nodo_actual]
            lat2, lon2 = self.posiciones[nodo_destino]
        
        # Si no se encuentran las coordenadas, retornamos 0
        except KeyError:
            # Si un nodo no tiene coordenadas (por seguridad), retornamos 0
            return 0

        # Convertir grados a radianes
        lat1, lon1 = map(radians, (lat1, lon1))
        lat2, lon2 = map(radians, (lat2, lon2))

        # Fórmula de Haversine
        dlon = lon2 - lon1 # Diferencia de longitud entre estaciones
        dlat = lat2 - lat1 # Diferencia de latitud entre estaciones
        # 'a' es el cuadrado de la mitad de la distancia entre las dos estaciones
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a)) #distancia angular en radianes
        r = 6371000  # Radio de la Tierra en metros
        
        distancia_recta = c * r #distancia = angulo * radio
        return distancia_recta

    def encontrar_ruta(self, estacion_origen_id, estacion_destino_id):
        # Método que ejecuta el algoritmo A*
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