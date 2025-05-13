import numpy as np


def get_cities():
    cities = {
        "Tangier": (-5.8, 35.8),
        "Tetouan": (-5.4, 35.6),
        "Larache": (-6.2, 35.2),
        "Chefchaouen": (-5.3, 35.2),
        "Hoceima": (-3.9, 35.2),
        "Kenitra": (-6.6, 34.3),
        "Rabat": (-6.8, 34.0),
        "Casablanca": (-7.6, 33.6),
        "Fes": (-5.0, 34.0),
        "Meknes": (-5.5, 33.9),
        "Oujda": (-1.9, 34.7),
        "Nador": (-2.9, 35.2),
        "Marrakesh": (-8.0, 31.6),
        "Agadir": (-9.6, 30.4),
        "Essaouira": (-9.8, 31.5),
        "Ouarzazate": (-6.9, 30.9),
        "El Jadida": (-8.5, 33.2),
        "Safi": (-9.2, 32.3),
        "Beni Mellal": (-6.4, 32.3),
        "Taza": (-4.0, 34.2),
        "Ifrane": (-5.1, 33.5),
        "Errachidia": (-4.4, 32.0),
    }
    return cities, len(cities)


def cities_to_array(cities_dict=None):
    if cities_dict is None:
        cities_dict, _ = get_cities()
        
    cities_names = list(cities_dict.keys())
    coordinates = np.array([cities_dict[name] for name in cities_names])
    return coordinates, cities_names


def load_city_data():
    print("\nLoading cities data...")
    cities_dict, num_cities = get_cities()
    cities_coordinates, cities_names = cities_to_array(cities_dict)
    print(f"Loaded {num_cities} cities for TSP.")
    
    return cities_coordinates, cities_names, num_cities
