#!/usr/bin/env python3
"""
Morocco Cities Visualization - Main entry point

This module serves as the main entry point for visualizing Moroccan cities
on a map for the Traveling Salesman Problem.
"""

import numpy as np
import time
import math

# Import modules from the project structure
from utils.cli import parse_arguments
from data.cities import get_cities, cities_to_array
from core.distance import compute_distance_matrix
from core.tour import nearest_neighbor_tour
from algorithms.tabu_search import tabu_search_optimization, calculate_tour_length
from utils.visualization import visualize_cities
from utils.tour_selection import select_cities_interactively, select_cities_randomly
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
    
    # Select cities for the tour based on mode
    if args.tour_selection:
        # Interactive selection mode
        start_city, selected_cities = select_cities_interactively(cities_names, num_cities)
    else:
        # Random selection mode
        start_city, selected_cities = select_cities_randomly(cities_names, num_cities, args.start_city)
    
    # Generate a tour using the nearest neighbor heuristic
    tour = nearest_neighbor_tour(distance_matrix, start_city, selected_cities)
    initial_length = calculate_tour_length(tour, distance_matrix)
    print(f"Nearest Neighbor Tour: {tour}")
    print(f"Starting City: {cities_names[tour[0]]}")
    print(f"Initial Tour Length: {initial_length:.2f}")
    
    # Apply tabu search optimization
    print("\nApplying tabu search optimization with 2-opt and city swap...")
    start_time = time.time()
    
    # Process dynamic tabu tenure based on problem size if specified
    if isinstance(args.tabu_tenure, str):
        if args.tabu_tenure.lower() == 'sqrt':
            tabu_tenure = int(round(math.sqrt(num_cities)))
            print(f"Using tabu tenure: sqrt({num_cities}) = {tabu_tenure}")
        elif args.tabu_tenure.lower() == 'log':
            tabu_tenure = int(round(math.log(num_cities) * 3))
            print(f"Using tabu tenure: log({num_cities}) * 3 = {tabu_tenure}")
        else:
            tabu_tenure = 10  # Default fallback
    else:
        tabu_tenure = args.tabu_tenure
    
    # Set max_no_improvement if not explicitly provided
    max_no_improvement = args.max_no_improvement if args.max_no_improvement is not None else tabu_tenure * 2
    
    print(f"Tabu tenure: {tabu_tenure}, Max iterations without improvement: {max_no_improvement}")
    
    # Set up performance tracking
    tracker = create_performance_tracker()
    progress_callback = create_progress_callback(tracker)
    
    # Run optimization with performance tracking
    optimized_tour, optimized_length, iterations, move_types = tabu_search_optimization(
        tour=tour,
        distance_matrix=distance_matrix,
        tabu_tenure=tabu_tenure,
        max_iterations=args.max_iterations,
        time_limit=args.time_limit,
        use_swap=not args.no_swap,
        prioritize_2opt=True,  # Always prioritize 2-opt by default
        aspiration_enabled=True,  # Always enable aspiration
        max_no_improvement=max_no_improvement,
        verbose=args.verbose,
        progress_callback=progress_callback
    )
    
    # Calculate optimization time
    optimization_time = time.time() - start_time
    
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
