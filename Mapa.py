import networkx as nx
from math import radians, cos, sin, asin, sqrt

class Mapa:
    #Constructor de Mapa,crear el grafo y  guarda las coordenadas de las estaciones
    def __init__(self):
        self.grafo = nx.Graph()
        self.posiciones = {}
        self.inicializar_mapa()
    #Funcion que se encarga de determinar el coste en funcion al peso de la arista,utiliza la formula
    #de Haversine para calcular la ditancia entre dos coordenadas
    def calcular_distancia(self, coord1, coord2):
        lat1, lon1 = map(radians, coord1)
        lat2, lon2 = map(radians, coord2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6371000  # Radio de la Tierra en metros
        return c * r
    
    #Funcion que define el grafo.Primero declara las estaciones y las aristas,establece las lineas 
    #, las ruta y los transbordos y luego los añade al grafo
    def inicializar_mapa(self):
        print("Cargando datos del Metro CDMX (Zona Recuadro Fucsia)...")
        datos_estaciones = {
            # LÍNEA 1 Observatorio - Balderas
            "Observatorio_L1": (19.3985, -99.2004),
            "Tacubaya_L1": (19.4032, -99.1871),
            "Juanacatlan_L1": (19.4129, -99.1821),
            "Chapultepec_L1": (19.4206, -99.1763),
            "Sevilla_L1": (19.4219, -99.1706),
            "Insurgentes_L1": (19.4236, -99.1629),
            "Cuauhtemoc_L1": (19.4259, -99.1547),
            "Balderas_L1": (19.4274, -99.1491),

            #LÍNEA 3 Universidad - Juárez
            "Universidad_L3": (19.3244, -99.1738),
            "Copilco_L3": (19.3359, -99.1766),
            "Miguel_Angel_de_Quevedo_L3": (19.3453, -99.1816),
            "Viveros_L3": (19.3537, -99.1764),
            "Coyoacan_L3": (19.3615, -99.1703),
            "Zapata_L3": (19.3706, -99.1653),
            "Division_del_Norte_L3": (19.3795, -99.1593),
            "Eugenia_L3": (19.3853, -99.1557),
            "Etiopia_L3": (19.3957, -99.1565),
            "Centro_Medico_L3": (19.4064, -99.1554),
            "Hospital_General_L3": (19.4143, -99.1538),
            "Ninos_Heroes_L3": (19.4207, -99.1508),
            "Balderas_L3": (19.4274, -99.1491), 
            "Juarez_L3": (19.4344, -99.1478),

            #LÍNEA 7 Barranca del Muerto - Polanco
            "Barranca_del_Muerto_L7": (19.3616, -99.1894),
            "Mixcoac_L7": (19.3757, -99.1873),
            "San_Antonio_L7": (19.3837, -99.1866),
            "San_Pedro_de_los_Pinos_L7": (19.3906, -99.1862),
            "Tacubaya_L7": (19.4032, -99.1880), 
            "Constituyentes_L7": (19.4124, -99.1920),
            "Auditorio_L7": (19.4242, -99.1922),
            "Polanco_L7": (19.4336, -99.1906),

            #LÍNEA 9 Tacubaya - Lázaro Cárdenas
            "Tacubaya_L9": (19.4030, -99.1875),
            "Patriotismo_L9": (19.4063, -99.1793),
            "Chilpancingo_L9": (19.4066, -99.1685),
            "Centro_Medico_L9": (19.4064, -99.1554),
            "Lazaro_Cardenas_L9": (19.4070, -99.1428),

            #LÍNEA 12 Mixcoac - Eje Central
            "Mixcoac_L12": (19.3757, -99.1873),
            "Insurgentes_Sur_L12": (19.3734, -99.1792),
            "Hospital_20_de_Noviembre_L12": (19.3725, -99.1721),
            "Zapata_L12": (19.3706, -99.1653),
            "Parque_de_los_Venados_L12": (19.3698, -99.1578),
            "Eje_Central_L12": (19.3688, -99.1481),
        }

        rutas = [
            # L1
            ["Observatorio_L1", "Tacubaya_L1", "Juanacatlan_L1", "Chapultepec_L1", 
             "Sevilla_L1", "Insurgentes_L1", "Cuauhtemoc_L1", "Balderas_L1"],
            # L3
            ["Universidad_L3", "Copilco_L3", "Miguel_Angel_de_Quevedo_L3", "Viveros_L3",
             "Coyoacan_L3", "Zapata_L3", "Division_del_Norte_L3", "Eugenia_L3",
             "Etiopia_L3", "Centro_Medico_L3", "Hospital_General_L3", "Ninos_Heroes_L3",
             "Balderas_L3", "Juarez_L3"],
            # L7
            ["Barranca_del_Muerto_L7", "Mixcoac_L7", "San_Antonio_L7", "San_Pedro_de_los_Pinos_L7",
             "Tacubaya_L7", "Constituyentes_L7", "Auditorio_L7", "Polanco_L7"],
            # L9
            ["Tacubaya_L9", "Patriotismo_L9", "Chilpancingo_L9", "Centro_Medico_L9", 
             "Lazaro_Cardenas_L9"],
            # L12
            ["Mixcoac_L12", "Insurgentes_Sur_L12", "Hospital_20_de_Noviembre_L12", 
             "Zapata_L12", "Parque_de_los_Venados_L12", "Eje_Central_L12"]
        ]

      
        for estacion_id, coords in datos_estaciones.items():
            self.grafo.add_node(estacion_id)
            self.posiciones[estacion_id] = coords
        
        for ruta in rutas:
            for i in range(len(ruta) - 1):
                origen = ruta[i]
                destino = ruta[i+1]
                
                # Calcular peso basado en distancia real
                peso = self.calcular_distancia(datos_estaciones[origen], datos_estaciones[destino])                
                self.grafo.add_edge(origen, destino, weight=peso)
        #Coste establecido al transbordo
        coste_transbordo = 180.0 

        transbordos = [
            ("Tacubaya_L1", "Tacubaya_L7"),
            ("Tacubaya_L1", "Tacubaya_L9"),
            ("Tacubaya_L7", "Tacubaya_L9"),
            ("Mixcoac_L7", "Mixcoac_L12"),
            ("Zapata_L3", "Zapata_L12"),
            ("Centro_Medico_L3", "Centro_Medico_L9"),
            ("Balderas_L1", "Balderas_L3")
        ]

        for t_origen, t_destino in transbordos:
            self.grafo.add_edge(t_origen, t_destino, weight=coste_transbordo)

        print(f"Mapa inicializado con {self.grafo.number_of_nodes()} estaciones y {self.grafo.number_of_edges()} conexiones.")

    def get_grafo(self):
        return self.grafo
    
    def get_posiciones(self):
        return self.posiciones