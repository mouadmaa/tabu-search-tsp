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
    
    # Initialize selected_cities as None (will include all cities by default)
    selected_cities = None
    
    # Handle tour selection if enabled
    if args.tour_selection:
        # Prompt user to choose a starting city
        print("\nInteractive Tour Selection Mode")
        print("------------------------------")
        print("Available cities:")
        for i, name in enumerate(cities_names):
            print(f"  {i+1}: {name}")
        
        # Get starting city with validation
        valid_start_city = False
        while not valid_start_city:
            try:
                start_city_input = input("\nEnter the index (1-22) of your starting city: ")
                start_idx = int(start_city_input) - 1  # Convert to 0-based index
                
                if 0 <= start_idx < num_cities:
                    start_city = start_idx
                    valid_start_city = True
                    print(f"Selected {cities_names[start_city]} as the starting city.")
                else:
                    print(f"Error: Please enter a valid index between 1 and {num_cities}.")
            except ValueError:
                print("Error: Please enter a valid integer.")
        
        # Let user select additional cities to visit
        print("\nNow select additional cities for your tour (at least 2 cities).")
        print("Enter 'q' when you're done selecting cities.")
        
        selected_cities = []
        while True:
            try:
                city_input = input(f"Enter city index (1-{num_cities}, excluding {start_city+1}) or 'q' to finish: ")
                
                if city_input.lower() == 'q':
                    # Check if we have at least 2 selected cities
                    if len(selected_cities) >= 2:
                        break
                    else:
                        print("Error: You must select at least 2 additional cities.")
                        continue
                
                city_idx = int(city_input) - 1  # Convert to 0-based index
                
                # Validate the selection
                if city_idx == start_city:
                    print(f"Error: You've already selected {cities_names[start_city]} as your starting city.")
                elif 0 <= city_idx < num_cities:
                    if city_idx in selected_cities:
                        print(f"Error: You've already selected {cities_names[city_idx]}.")
                    else:
                        selected_cities.append(city_idx)
                        print(f"Added {cities_names[city_idx]} to your tour. "
                              f"({len(selected_cities)} cities selected so far)")
                else:
                    print(f"Error: Please enter a valid index between 1 and {num_cities}.")
            except ValueError:
                if city_input.lower() == 'q':
                    if len(selected_cities) >= 2:
                        break
                    else:
                        print("Error: You must select at least 2 additional cities.")
                else:
                    print("Error: Please enter a valid integer or 'q'.")
        
        print(f"\nTour will include the starting city {cities_names[start_city]} and {len(selected_cities)} additional cities:")
        for idx in selected_cities:
            print(f"  - {cities_names[idx]}")
    else:
        # Use a specified start city if provided, otherwise random
        start_city = args.start_city
        if start_city is not None:
            if start_city < 0 or start_city >= num_cities:
                print(f"Warning: Start city index {start_city} is out of range (0-{num_cities-1}). Using random start city.")
                start_city = None
            else:
                print(f"Using city {start_city} ({cities_names[start_city]}) as starting point.")
        else:
            # Select a random starting city
            start_city = np.random.randint(0, num_cities)
            print(f"Randomly selected {cities_names[start_city]} as the starting city.")
        
        # In automatic mode (default), randomly select a subset of cities to visit
        # First create a list of all cities except the starting city
        all_cities_except_start = list(range(num_cities))
        all_cities_except_start.remove(start_city)
        
        # Randomly decide how many cities to visit (between 2 and num_cities-1)
        # The -1 is because we already have the starting city
        num_cities_to_select = np.random.randint(2, num_cities)
        
        # Randomly select the cities
        selected_cities = np.random.choice(
            all_cities_except_start, 
            size=min(num_cities_to_select, len(all_cities_except_start)), 
            replace=False
        ).tolist()
        
        print(f"\nRandomly selected {len(selected_cities)} cities to visit (excluding starting city):")
        for idx in selected_cities:
            print(f"  - {cities_names[idx]}")
    
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
    
    # Create a performance tracker
    from utils.performance_tracker import PerformanceTracker
    tracker = PerformanceTracker()
    tracker.start()
    
    # Create a callback for performance tracking
    def track_progress(iteration, current_tour, current_length, best_tour, best_length, move_info):
        move_type = move_info[0] if move_info else None
        tracker.track_iteration(iteration, current_length, best_length, move_type)
    
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
        progress_callback=track_progress  # Add a progress callback for tracking
    )
    
    optimization_time = time.time() - start_time
    improvement = initial_length - optimized_length
    improvement_percentage = (improvement / initial_length) * 100
    
    print(f"\nTabu search optimization completed in {optimization_time:.2f} seconds.")
    print(f"Iterations performed: {iterations}")
    print(f"Move types used for improvements: 2-opt: {move_types['2opt']}, swap: {move_types['swap']}")
    print(f"Initial tour length: {initial_length:.2f}")
    print(f"Optimized tour length: {optimized_length:.2f}")
    print(f"Improvement: {improvement:.2f} ({improvement_percentage:.2f}%)")
    
    # Display performance summary and visualization if requested
    print(f"\n{tracker.get_summary()}")
    
    if args.show_performance or args.save_performance:
        import matplotlib.pyplot as plt
        title = "Tabu Search Performance for Morocco Cities"
        tracker.show_report(title=title, save_path=args.save_performance)
        
        if args.show_performance:
            plt.show()

    
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
