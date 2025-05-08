"""
Distance calculation module for the Traveling Salesman Problem.

This module provides functions to compute distances between cities.
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
