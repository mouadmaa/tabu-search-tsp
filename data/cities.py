"""
Module containing Moroccan city data for the Traveling Salesman Problem.

This module provides functions to access a predefined set of Moroccan cities
with their coordinates in (longitude, latitude) format, suitable for
visualization and TSP algorithm implementation.
"""

import numpy as np


def get_cities():
    """
    Returns a dictionary with major Moroccan cities and their simplified coordinates
    in a longitude/latitude format.
    
    Returns:
        dict: Dictionary mapping city names to (longitude, latitude) coordinate tuples
    """
    # Morocco longitude range: approximately -10 to -1
    # Morocco latitude range: approximately 30 to 36
    # Coordinates are simplified but proportionally resemble real positions
    morocco_cities = {
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
    return morocco_cities


def cities_to_array(cities_dict=None):
    """
    Converts the dictionary of Moroccan cities to a NumPy array format
    suitable for TSP algorithms and returns a list of city names in the same order.
    
    Args:
        cities_dict (dict, optional): Dictionary mapping city names to (x,y) coordinates.
                                     If None, uses the default Morocco cities.
        
    Returns:
        tuple: (numpy.ndarray of shape (num_cities, 2), list of city names)
    """
    if cities_dict is None:
        cities_dict = get_cities()
        
    city_names = list(cities_dict.keys())
    coordinates = np.array([cities_dict[name] for name in city_names])
    return coordinates, city_names
