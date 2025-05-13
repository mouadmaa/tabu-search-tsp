#!/usr/bin/env python3

from utils.cli import parse_arguments
from data.cities import load_city_data
from core.distance import compute_distance_matrix
from utils.tour_selection import create_initial_tour
from core.performance import optimize_tour
from core.visualization import visualize_results


def main():
    print("\nTraveling Salesman Problem Using Tabu Search Optimization\n")

    args = parse_arguments()

    cities_coordinates, cities_names, num_cities = load_city_data()

    distance_matrix = compute_distance_matrix(cities_coordinates)

    tour, initial_length, start_city = create_initial_tour(
        distance_matrix, cities_names, num_cities, args.tour_selection
    )
    
    optimized_tour, optimized_length = optimize_tour(
        tour, distance_matrix, args, initial_length, cities_names
    )
    
    visualize_results(
        cities_coordinates, cities_names, tour, optimized_tour, args.tour_selection
    )
    
    print("\nDone.")


if __name__ == "__main__":
    main()
