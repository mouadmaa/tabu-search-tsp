"""
Module containing functions for initializing tours for the Traveling Salesman Problem.

This module provides functions to generate initial tours using the nearest neighbor heuristic.
"""

import numpy as np


def nearest_neighbor_tour(distance_matrix, start_city=None):
    """
    Generate a tour using the nearest neighbor heuristic.
    
    Args:
        distance_matrix (numpy.ndarray): Matrix of distances between cities
        start_city (int, optional): Index of the starting city. If None, a random city is chosen.
        
    Returns:
        list: A tour generated using the nearest neighbor heuristic
    """
    num_cities = distance_matrix.shape[0]
    
    # Choose a random starting city if not specified
    if start_city is None:
        start_city = np.random.randint(0, num_cities)
    
    # Initialize the tour with the starting city
    tour = [start_city]
    unvisited = set(range(num_cities))
    unvisited.remove(start_city)
    
    # Build the tour by always selecting the closest unvisited city
    current_city = start_city
    while unvisited:
        # Find the closest unvisited city to the current city
        distances = [(distance_matrix[current_city, j], j) for j in unvisited]
        _, next_city = min(distances)
        
        # Add the closest city to the tour
        tour.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city
        
    return tour


def calculate_tour_length(cities_coordinates, tour):
    """
    Calculate the total length of a tour.

    Args:
        cities_coordinates (numpy.ndarray): Array of shape (num_cities, 2) with city coordinates
        tour (list): List of city indices representing a TSP route

    Returns:
        float: Total length of the tour
    """
    total_length = 0.0

    # Calculate the distance between consecutive cities in the tour
    for i in range(len(tour)):
        from_city = tour[i]
        to_city = tour[(i + 1) % len(tour)]  # Wrap around to the first city

        # Calculate Euclidean distance
        distance = np.sqrt(np.sum((cities_coordinates[from_city] - cities_coordinates[to_city]) ** 2))
        total_length += distance

    return total_length
