import json
from geopy.distance import geodesic
from shapely.geometry import Point, Polygon

# Leer el archivo GeoJSON que contiene los datos de las geocercas
with open('geofences.geojson') as archivo:
    geofences_data = json.load(archivo)

# Crear una lista para almacenar los polígonos de las geocercas y sus propiedades
geofence_polygons = []
geofence_properties = []

# Extraer las coordenadas y propiedades de cada geocerca y crear polígonos
for caracteristica in geofences_data['features']:
    coordenadas = caracteristica['geometry']['coordinates'][0]
    poligono = Polygon(coordenadas)
    geofence_polygons.append(poligono)
    propiedades = caracteristica['properties']
    geofence_properties.append(propiedades)

# Definir un conjunto de puntos para calcular distancias y encontrar la geocerca más cercana
puntos = [
    {'nombre': 'Punto A', 'coordenadas': (37.7749, -122.4194)},
    {'nombre': 'Punto B', 'coordenadas': (-71.281, 40.748)},
    {'nombre': 'Punto C', 'coordenadas': (34.0522, -118.2437)},
    {'nombre': 'Punto D', 'coordenadas': (-118.26557159423828, 34.04553686521083)},

]

# Iterar a través de cada punto y encontrar la geocerca más cercana
for punto in puntos:
    coordenadas_punto = punto['coordenadas']
    punto_a_verificar = Point(coordenadas_punto)

    indice_geocerca_mas_cercana = None
    distancia_mas_cercana = float('inf')

    for indice, poligono in enumerate(geofence_polygons):
        if poligono.contains(punto_a_verificar):
            indice_geocerca_mas_cercana = indice
            distancia_mas_cercana = 0.0
            break

        distancia = poligono.distance(punto_a_verificar)
        if distancia < distancia_mas_cercana:
            indice_geocerca_mas_cercana = indice
            distancia_mas_cercana = distancia

    if indice_geocerca_mas_cercana is not None:
        propiedades_geocerca_mas_cercana = geofence_properties[indice_geocerca_mas_cercana]
        nombre_geocerca_mas_cercana = propiedades_geocerca_mas_cercana['name']
        if distancia_mas_cercana == 0.0:
            print(f"{punto['nombre']} está dentro de {nombre_geocerca_mas_cercana}")
        else:
            print(f"{punto['nombre']} está a {distancia_mas_cercana:.2f} metros de {nombre_geocerca_mas_cercana}")
    else:
        print(f"No existe geocerca para {punto['nombre']}")
