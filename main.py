#!/usr/bin/env python3
"""
Morocco Cities Visualization - Main entry point

This module serves as the main entry point for visualizing Moroccan cities
on a map for the Traveling Salesman Problem.
"""

import numpy as np
import argparse

# Import modules from the project structure
from data.cities import get_morocco_cities, morocco_cities_to_array
from core.distance import compute_distance_matrix
from utils.visualization import visualize_cities


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Visualize Moroccan cities for the Traveling Salesman Problem')
    
    parser.add_argument('--save-plot', action='store_true',
                        help='Save the visualization to a file instead of displaying it')
    parser.add_argument('--output', type=str, default='morocco_cities.png',
                        help='Output filename for the visualization (if --save-plot is used)')
    parser.add_argument('--verbose', action='store_true',
                        help='Print detailed progress information')
    
    return parser.parse_args()


def main():
    """
    Main function to display Moroccan cities on a map.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Print welcome message
    print("=" * 80)
    print("Morocco Cities Visualization for Traveling Salesman Problem")
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
    
    # Visualize the cities on a map (without any route yet)
    print("\nVisualizing Moroccan cities...")
    visualize_cities(
        cities=cities,
        city_names=city_names,
        title="Moroccan Cities for TSP",
        save_to_file=args.save_plot,
        filename=args.output
    )
    
    if args.save_plot:
        print(f"Visualization saved to {args.output}")
    else:
        print("Displaying visualization. Close the window to exit.")
    
    print("\nDone.")


if __name__ == "__main__":
    main()
