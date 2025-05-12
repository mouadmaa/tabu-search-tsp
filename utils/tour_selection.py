"""
Tour selection module for the Traveling Salesman Problem.

This module handles the selection of cities for the TSP tour,
providing both interactive user selection and random selection functionality.
"""

import numpy as np


def select_cities_interactively(cities_names, num_cities):
    """
    Prompt the user to select cities interactively.
    
    Args:
        cities_names (list): List of city names
        num_cities (int): Total number of available cities
        
    Returns:
        tuple: (int: starting city index, list: indices of additional cities to visit)
    """
    print("\nInteractive Tour Selection Mode")
    print("------------------------------")
    print("Available cities:")
    for i, name in enumerate(cities_names):
        print(f"  {i+1}: {name}")
    
    # Get starting city with validation
    valid_start_city = False
    start_city = None
    
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
    
    return start_city, selected_cities


def select_cities_randomly(cities_names, num_cities):
    """
    Randomly select cities for the tour.
    
    Args:
        cities_names (list): List of city names
        num_cities (int): Total number of available cities
        
    Returns:
        tuple: (int: starting city index, list: indices of additional cities to visit)
    """
    # Select a random starting city
    start_city = np.random.randint(0, num_cities)
    print(f"Randomly selected {cities_names[start_city]} as the starting city.")

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
    
    return start_city, selected_cities


def display_tour_cities(tour, cities_names, is_interactive=False, initial_length=None):
    """
    Display the selected cities in a horizontal format.
    
    Args:
        tour (list): The tour containing city indices
        cities_names (list): List of all city names
        is_interactive (bool): Whether the tour was selected interactively
        initial_length (float, optional): Initial tour length to display
    """
    # Get the names of the selected cities (excluding the starting city)
    selected_city_names = [cities_names[i] for i in tour[1:]]
    
    # Format for display with cities side by side
    city_mode = "Selected" if is_interactive else "Randomly selected"
    print(f"{city_mode} {len(selected_city_names)} cities to visit:")
    
    # Display cities in rows with multiple cities per row
    cities_per_row = 4
    for i in range(0, len(selected_city_names), cities_per_row):
        row_cities = selected_city_names[i:i+cities_per_row]
        formatted_cities = ", ".join(row_cities)
        print(f"  {formatted_cities}")
    
    # Display initial tour length if provided
    if initial_length is not None:
        print(f"Initial Tour Length: {initial_length:.2f}")
