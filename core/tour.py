import numpy as np


def nearest_neighbor_tour(distance_matrix, start_city=None, selected_cities=None):
    num_cities = distance_matrix.shape[0]
    
    if start_city is None:
        start_city = np.random.randint(0, num_cities)
    
    tour = [start_city]
    
    if selected_cities is None:
        unvisited = set(range(num_cities))
        unvisited.remove(start_city)
    else:
        unvisited = set(selected_cities)
        if start_city in unvisited:
            unvisited.remove(start_city)
    
    current_city = start_city
    while unvisited:
        distances = [(distance_matrix[current_city, j], j) for j in unvisited]
        _, next_city = min(distances)
        
        tour.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city
        
    return tour


def calculate_tour_length(cities_coordinates, tour):
    total_length = 0.0

    for i in range(len(tour)):
        from_city = tour[i]
        to_city = tour[(i + 1) % len(tour)]

        distance = np.sqrt(np.sum((cities_coordinates[from_city] - cities_coordinates[to_city]) ** 2))
        total_length += distance

    return total_length
