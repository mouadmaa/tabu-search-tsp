#!/usr/bin/env python3
"""
Morocco Cities Visualization - Main entry point

This module serves as the main entry point for the Traveling Salesman Problem (TSP)
visualization using Tabu Search optimization for Moroccan cities.
"""

# Core imports
from utils.cli import parse_arguments
from data.cities import load_city_data
from core.distance import compute_distance_matrix
from utils.tour_selection import create_initial_tour
from core.performance import optimize_tour
from core.visualization import visualize_results


def main():
    """Main application entry point."""

    # Parse arguments
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
        tour, distance_matrix, args, initial_length, cities_names
    )
    
    # Visualize the optimized results
    visualize_results(
        cities_coordinates, cities_names, tour, optimized_tour, args.tour_selection
    )
    
    print("\nDone.")


if __name__ == "__main__":
    main()
