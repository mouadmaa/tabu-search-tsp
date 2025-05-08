"""
Distance calculation module for the Traveling Salesman Problem.

This module provides functions to compute distances between cities
and calculate the total distance of TSP routes.
"""

import numpy as np


def compute_distance_matrix(cities):
    """
    Compute the Euclidean distance matrix between all pairs of cities.
    
    Args:
        cities (numpy.ndarray): Array of shape (num_cities, 2) with city coordinates
        
    Returns:
        numpy.ndarray: Distance matrix of shape (num_cities, num_cities)
    """
    num_cities = cities.shape[0]
    distance_matrix = np.zeros((num_cities, num_cities))
    
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                # Calculate Euclidean distance between cities i and j
                distance_matrix[i, j] = np.sqrt(
                    np.sum((cities[i] - cities[j]) ** 2)
                )
    
    return distance_matrix


def calculate_route_distance(route, distance_matrix):
    """
    Calculate the total distance of a TSP route.
    
    Args:
        route (list): List of city indices representing a route
        distance_matrix (numpy.ndarray): Distance matrix between cities
        
    Returns:
        float: Total distance of the route
    """
    total_distance = 0
    num_cities = len(route)
    
    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]  # Wrap around to the first city
        total_distance += distance_matrix[from_city, to_city]
    
    return total_distance
