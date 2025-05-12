#!/usr/bin/env python3
"""
Morocco Cities Visualization - Main entry point

This module serves as the main entry point for visualizing Moroccan cities
on a map for the Traveling Salesman Problem.
"""

import numpy as np
import time

# Import modules from the project structure
from utils.cli import parse_arguments
from data.cities import get_cities, cities_to_array
from core.distance import compute_distance_matrix
from core.tour import nearest_neighbor_tour
from algorithms.tabu_search import tabu_search_optimization, calculate_tour_length, process_tabu_tenure
from utils.visualization import visualize_cities
from utils.tour_selection import select_cities_interactively, select_cities_randomly, display_tour_cities
from utils.performance_manager import create_performance_tracker, create_progress_callback, display_performance_results


def main():
    """
    Main function to display Moroccan cities on a map.
    """
    # Parse command line arguments
    args = parse_arguments()

    # Print a welcome message
    print("=" * 80)
    print("Morocco Cities Visualization for Traveling Salesman Problem")
    print("Using Tabu Search optimization")
    print("=" * 80)
    
    # Load Moroccan cities
    print("\nLoading Moroccan city data...")
    cities_dict, num_cities = get_cities()
    cities_coordinates, cities_names = cities_to_array(cities_dict)

    print(f"Loaded {num_cities} Moroccan cities for TSP.")

    # Compute distance matrix
    print("\nComputing distance matrix...")
    distance_matrix = compute_distance_matrix(cities_coordinates)
    print("Distance matrix computed.")
    
    # Generate initial tour using nearest neighbor heuristic
    print("\nGenerating nearest neighbor tour...")
    
    # Select cities for the tour based on mode
    if args.tour_selection:
        # Interactive selection mode
        start_city, selected_cities = select_cities_interactively(cities_names, num_cities)
    else:
        # Random selection mode
        start_city, selected_cities = select_cities_randomly(cities_names, num_cities)
    
    # Generate a tour using the nearest neighbor heuristic
    tour = nearest_neighbor_tour(distance_matrix, start_city, selected_cities)
    initial_length = calculate_tour_length(tour, distance_matrix)
    
    # Display selected cities using the tour_selection module
    display_tour_cities(tour, cities_names, is_interactive=args.tour_selection, initial_length=initial_length)
    
    # Apply tabu search optimization
    print("\nApplying tabu search optimization...")
    start_time = time.time()
    
    # Set up performance tracking
    tracker = create_performance_tracker()
    progress_callback = create_progress_callback(tracker, initial_tour_length=initial_length)
    
    # Run optimization with performance tracking
    optimized_tour, optimized_length, iterations, move_types = tabu_search_optimization(
        tour=tour,
        distance_matrix=distance_matrix,
        tabu_tenure=args.tabu_tenure,
        max_iterations=args.max_iterations,
        time_limit=args.time_limit,
        max_no_improvement=args.max_no_improvement,
        progress_callback=progress_callback
    )
    
    # Calculate optimization time
    optimization_time = time.time() - start_time
    print("Optimization completed.")
    
    # Display performance results
    display_performance_results(
        tracker, initial_length, optimized_length, 
        iterations, move_types, optimization_time, args
    )
    
    # Visualize the cities on a map with the optimized tour
    tour_mode = "User-Selected" if args.tour_selection else f"Random ({len(tour)} cities)"
    visualization_title = f"Moroccan Cities for TSP with Tabu Search Optimized Tour ({tour_mode})"
    print(f"\nVisualizing Moroccan cities with optimized tour...")
    visualize_cities(
        cities_coordinates=cities_coordinates,
        cities_names=cities_names,
        title=visualization_title,
        save_to_file=args.save_plot,
        filename=args.output,
        route=optimized_tour,
        start_city_idx=tour[0]
    )
    
    if args.save_plot:
        print(f"Visualization saved to {args.output}")
    else:
        print("Displaying visualization. Close the window to exit.")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
