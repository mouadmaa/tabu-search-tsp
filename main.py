#!/usr/bin/env python3
"""
Morocco Cities Visualization - Main entry point

This module serves as the main entry point for the Traveling Salesman Problem (TSP)
visualization using Tabu Search optimization for Moroccan cities.
"""

import time

# Core imports
from utils.cli import parse_arguments
from data.cities import get_cities, cities_to_array
from core.distance import compute_distance_matrix
from core.tour import nearest_neighbor_tour
from algorithms.tabu_search import tabu_search_optimization, calculate_tour_length
from utils.visualization import visualize_cities
from utils.tour_selection import select_cities_interactively, select_cities_randomly, display_tour_cities
from utils.performance import create_performance_tracker, create_progress_callback, display_performance_results


def load_city_data():
    """Load and prepare Moroccan city data."""
    print("\nLoading Moroccan city data...")
    cities_dict, num_cities = get_cities()
    cities_coordinates, cities_names = cities_to_array(cities_dict)
    print(f"Loaded {num_cities} Moroccan cities for TSP.")
    
    return cities_coordinates, cities_names, num_cities


def create_initial_tour(distance_matrix, cities_names, num_cities, interactive_mode):
    """Create initial tour using nearest neighbor approach with selected cities."""
    print("\nGenerating nearest neighbor tour...")
    
    if interactive_mode:
        start_city, selected_cities = select_cities_interactively(cities_names, num_cities)
    else:
        start_city, selected_cities = select_cities_randomly(cities_names, num_cities)
    
    tour = nearest_neighbor_tour(distance_matrix, start_city, selected_cities)
    initial_length = calculate_tour_length(tour, distance_matrix)
    
    # Display tour information
    display_tour_cities(tour, cities_names, is_interactive=interactive_mode, initial_length=initial_length)
    
    return tour, initial_length, start_city


def optimize_tour(tour, distance_matrix, args, initial_length):
    """Run Tabu Search optimization on the tour."""
    print("\nApplying tabu search optimization...")
    start_time = time.time()
    
    # Setup performance tracking
    tracker = create_performance_tracker()
    progress_callback = create_progress_callback(tracker, initial_tour_length=initial_length)
    
    # Run optimization
    optimized_tour, optimized_length, iterations, move_types = tabu_search_optimization(
        tour=tour,
        distance_matrix=distance_matrix,
        tabu_tenure=args.tabu_tenure,
        max_iterations=args.max_iterations,
        time_limit=args.time_limit,
        max_no_improvement=args.max_no_improvement,
        progress_callback=progress_callback
    )
    
    optimization_time = time.time() - start_time
    print("Optimization completed.")
    
    # Display results
    display_performance_results(
        tracker, initial_length, optimized_length, 
        iterations, move_types, optimization_time, args
    )
    
    return optimized_tour, optimized_length


def visualize_results(cities_coordinates, cities_names, tour, optimized_tour, is_interactive):
    """Visualize the optimized tour on a map."""
    tour_mode = "User-Selected" if is_interactive else f"Random ({len(tour)} cities)"
    title = f"Moroccan Cities TSP - Tabu Search Optimized Tour ({tour_mode})"
    
    print(f"\nVisualizing Moroccan cities with optimized tour...")
    print("Displaying visualization. Close the window to exit.")
    
    visualize_cities(
        cities_coordinates=cities_coordinates,
        cities_names=cities_names,
        title=title,
        route=optimized_tour,
        start_city_idx=tour[0]
    )


def main():
    """Main application entry point."""
    # Parse arguments and display a welcome message
    args = parse_arguments()
    
    print("=" * 80)
    print("Morocco Cities Visualization for Traveling Salesman Problem")
    print("Using Tabu Search optimization")
    print("=" * 80)
    
    # Load city data
    cities_coordinates, cities_names, num_cities = load_city_data()
    
    # Compute distance matrix
    print("\nComputing distance matrix...")
    distance_matrix = compute_distance_matrix(cities_coordinates)
    print("Distance matrix computed.")
    
    # Create an initial tour
    tour, initial_length, start_city = create_initial_tour(
        distance_matrix, cities_names, num_cities, args.tour_selection
    )
    
    # Optimize tour using Tabu Search
    optimized_tour, optimized_length = optimize_tour(
        tour, distance_matrix, args, initial_length
    )
    
    # Visualize the optimized results
    visualize_results(
        cities_coordinates, cities_names, tour, optimized_tour, args.tour_selection
    )
    
    print("\nDone.")


if __name__ == "__main__":
    main()
