#!/usr/bin/env python3
"""
Morocco TSP Solver - Main entry point

This module serves as the main entry point for the Morocco Traveling Salesman Problem solver.
It loads city data, runs the Tabu Search algorithm, and visualizes the results.
"""

import numpy as np
import argparse
import time

# Import modules from the project structure
from data.cities import get_morocco_cities, morocco_cities_to_array
from core.distance import compute_distance_matrix, calculate_route_distance
from utils.visualization import visualize_cities, plot_performance
from algorithms.tabu_search import solve_tsp


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Solve the Traveling Salesman Problem for Moroccan cities')
    
    parser.add_argument('--iterations', type=int, default=200,
                        help='Maximum number of iterations for the Tabu Search algorithm')
    parser.add_argument('--tabu-tenure', type=int, default=15,
                        help='Tabu tenure (how long a move remains tabu)')
    parser.add_argument('--save-plot', action='store_true',
                        help='Save the visualization to a file instead of displaying it')
    parser.add_argument('--output', type=str, default='morocco_tsp_solution.png',
                        help='Output filename for the visualization (if --save-plot is used)')
    parser.add_argument('--verbose', action='store_true',
                        help='Print detailed progress information')
    parser.add_argument('--no-plot-performance', action='store_true',
                        help='Do not plot the performance graph')
    
    return parser.parse_args()


def main():
    """
    Main function to run the TSP solver.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Print welcome message
    print("=" * 80)
    print("Traveling Salesman Problem Solver for Moroccan Cities")
    print("=" * 80)
    
    # Load Moroccan cities
    print("\nLoading Moroccan city data...")
    morocco_cities_dict = get_morocco_cities()
    cities, city_names = morocco_cities_to_array(morocco_cities_dict)
    
    print(f"Loaded {len(city_names)} Moroccan cities for TSP:")
    for i, name in enumerate(city_names):
        print(f"  {i}: {name} at (longitude, latitude): ({cities[i, 0]:.2f}, {cities[i, 1]:.2f})")
    
    # Compute distance matrix
    print("\nComputing distance matrix...")
    distance_matrix = compute_distance_matrix(cities)
    print("Distance matrix computed.")
    
    if args.verbose:
        print("\nDistance Matrix (first 5x5 entries):")
        np.set_printoptions(precision=2, suppress=True)
        print(distance_matrix[:5, :5])
    
    # Solve TSP using Tabu Search
    print(f"\nSolving TSP using Tabu Search (max iterations: {args.iterations}, tabu tenure: {args.tabu_tenure})...")
    start_time = time.time()
    
    best_route, best_distance, tabu_search = solve_tsp(
        distance_matrix=distance_matrix,
        tabu_tenure=args.tabu_tenure,
        max_iterations=args.iterations,
        verbose=args.verbose
    )
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Display results
    print("\nTSP Solution:")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Best route length: {best_distance:.2f} distance units")
    
    print("\nRoute sequence:")
    for i, city_idx in enumerate(best_route):
        print(f"  {i+1}. {city_names[city_idx]}")
    print(f"  Return to {city_names[best_route[0]]}")  # Return to start
    
    # Plot performance if requested
    if not args.no_plot_performance:
        print("\nPlotting optimization performance...")
        plot_performance(
            tabu_search.iterations,
            tabu_search.distances,
            tabu_search.best_distances,
            title="Tabu Search Optimization Progress"
        )
    
    # Visualize solution
    print("\nVisualizing TSP solution...")
    visualize_cities(
        cities=cities,
        city_names=city_names,
        title=f"TSP Solution for Morocco: {best_distance:.2f} distance units",
        save_to_file=args.save_plot,
        filename=args.output,
        route=best_route
    )
    
    if args.save_plot:
        print(f"Visualization saved to {args.output}")
    else:
        print("Displaying visualization. Close the window to exit.")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
