import numpy as np


def compute_distance_matrix(cities):
    print("\nComputing distance matrix...")

    num_cities = cities.shape[0]
    distance_matrix = np.zeros((num_cities, num_cities))
    
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                # Euclidean distance sqrt((x2 - x1)^2 + (y2 - y1)^2)
                distance_matrix[i, j] = np.sqrt(
                    np.sum((cities[i] - cities[j]) ** 2)
                )

    print("Distance matrix computed.")

    return distance_matrix
