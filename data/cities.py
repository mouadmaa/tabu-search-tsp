"""
Module containing Moroccan city data for the Traveling Salesman Problem.

This module provides functions to access a predefined set of Moroccan cities
with their coordinates in (longitude, latitude) format, suitable for
visualization and TSP algorithm implementation.
"""

import numpy as np


def get_morocco_cities():
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
        "Tangier": (-5.8, 35.8),       # Northern city
        "Tetouan": (-5.4, 35.6),       # Northern city, east of Tangier
        "Chefchaouen": (-5.3, 35.2),   # Northern, in the Rif mountains
        "Rabat": (-6.8, 34.0),         # Capital, on the Atlantic coast
        "Casablanca": (-7.6, 33.6),    # Major city on the Atlantic coast
        "Fes": (-5.0, 34.0),           # Northeast inland
        "Meknes": (-5.5, 33.9),        # Near Fes
        "Oujda": (-1.9, 34.7),         # Far eastern city, near Algeria
        "Nador": (-2.9, 35.2),         # Northeastern coastal city
        "Marrakesh": (-8.0, 31.6),     # Central, inland city
        "Agadir": (-9.6, 30.4),        # Southwestern coastal city
        "Essaouira": (-9.8, 31.5),     # Western coastal city
        "Ouarzazate": (-6.9, 30.9),    # South central, gateway to the desert
        "El Jadida": (-8.5, 33.2),     # Western coastal city
        "Safi": (-9.2, 32.3),          # Western coastal city
        "Beni Mellal": (-6.4, 32.3),   # Central inland city
        "Taza": (-4.0, 34.2),          # Northeastern city
        "Ifrane": (-5.1, 33.5),        # Middle Atlas mountain town
        "Larache": (-6.2, 35.2),       # Northern coastal city
        "Kenitra": (-6.6, 34.3),       # Atlantic coastal city north of Rabat
        "Hoceima": (-3.9, 35.2)        # Northern coastal city on Mediterranean
    }
    return morocco_cities


def morocco_cities_to_array(cities_dict=None):
    """
    Converts the dictionary of Moroccan cities to a NumPy array format
    suitable for TSP algorithms, and returns a list of city names in the same order.
    
    Args:
        cities_dict (dict, optional): Dictionary mapping city names to (x,y) coordinates.
                                     If None, uses the default Morocco cities.
        
    Returns:
        tuple: (numpy.ndarray of shape (num_cities, 2), list of city names)
    """
    if cities_dict is None:
        cities_dict = get_morocco_cities()
        
    city_names = list(cities_dict.keys())
    coordinates = np.array([cities_dict[name] for name in city_names])
    return coordinates, city_names


def generate_random_cities(num_cities, seed=None, x_range=(0, 100), y_range=(0, 100)):
    """
    Generate random city coordinates in a 2D plane.
    
    Args:
        num_cities (int): Number of cities to generate
        seed (int, optional): Random seed for reproducibility
        x_range (tuple): Range for x coordinates (min, max)
        y_range (tuple): Range for y coordinates (min, max)
        
    Returns:
        numpy.ndarray: Array of shape (num_cities, 2) with city coordinates
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate random coordinates
    x_coords = np.random.uniform(x_range[0], x_range[1], num_cities)
    y_coords = np.random.uniform(y_range[0], y_range[1], num_cities)
    
    # Combine into a single array
    cities = np.column_stack((x_coords, y_coords))
    
    return cities
