#!/usr/bin/env python3
"""
Morocco Cities Visualization - Main entry point

This module serves as the main entry point for visualizing Moroccan cities
on a map for the Traveling Salesman Problem.
"""

import numpy as np

# Import modules from the project structure
from utils.cli import parse_arguments
from data.cities import get_cities, cities_to_array
from core.distance import compute_distance_matrix
from core.tour_initialization import nearest_neighbor_tour
from utils.visualization import visualize_cities


def main():
    """
    Main function to display Moroccan cities on a map.
    """

    # Parse command line arguments
    args = parse_arguments()

    # Print a welcome message
    print("=" * 80)
    print("Morocco Cities Visualization for Traveling Salesman Problem")
    print("=" * 80)
    
    # Load Moroccan cities
    print("\nLoading Moroccan city data...")
    cities_dict, num_cities = get_cities()
    cities_coordinates, cities_names = cities_to_array(cities_dict)

    print(f"Loaded {num_cities} Moroccan cities for TSP:")
    for i, name in enumerate(cities_names):
        print(f"  {i}: {name} at (longitude, latitude): ({cities_coordinates[i, 0]:.2f}, {cities_coordinates[i, 1]:.2f})")
    
    # Compute distance matrix
    print("\nComputing distance matrix...")
    distance_matrix = compute_distance_matrix(cities_coordinates)
    print("Distance matrix computed.")
    
    if args.verbose:
        print("\nDistance Matrix (first 5x5 entries):")
        np.set_printoptions(precision=2, suppress=True)
        print(distance_matrix[:5, :5])
    
    # Generate initial tour using nearest neighbor heuristic
    print("\nGenerating nearest neighbor tour...")
    
    # Use a specified start city if provided, otherwise random
    start_city = args.start_city
    if start_city is not None:
        if start_city < 0 or start_city >= num_cities:
            print(f"Warning: Start city index {start_city} is out of range (0-{num_cities-1}). Using random start city.")
            start_city = None
        else:
            print(f"Using city {start_city} ({cities_names[start_city]}) as starting point.")
    
    # Generate a tour using the nearest neighbor heuristic
    tour = nearest_neighbor_tour(distance_matrix, start_city)
    print(f"Nearest Neighbor Tour: {tour}")
    print(f"Starting City: {cities_names[tour[0]]}")
    
    # Visualize the cities on a map with the tour
    print("\nVisualizing Moroccan cities with nearest neighbor tour...")
    visualize_cities(
        cities_coordinates=cities_coordinates,
        cities_names=cities_names,
        title="Moroccan Cities for TSP with Nearest Neighbor Tour",
        save_to_file=args.save_plot,
        filename=args.output,
        route=tour
    )
    
    if args.save_plot:
        print(f"Visualization saved to {args.output}")
    else:
        print("Displaying visualization. Close the window to exit.")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
