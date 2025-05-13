import numpy as np
from core.tour import nearest_neighbor_tour
from algorithms.tabu_search import calculate_tour_length


def select_cities_interactively(cities_names, num_cities):
    print("\nInteractive Tour Selection Mode")
    print("------------------------------")
    print("Available cities:")
    for i, name in enumerate(cities_names):
        print(f"  {i+1}: {name}")
    
    valid_start_city = False
    start_city = None
    
    while not valid_start_city:
        try:
            start_city_input = input("\nEnter the index (1-22) of your starting city: ")
            start_idx = int(start_city_input) - 1
            
            if 0 <= start_idx < num_cities:
                start_city = start_idx
                valid_start_city = True
                print(f"Selected {cities_names[start_city]} as the starting city.")
            else:
                print(f"Error: Please enter a valid index between 1 and {num_cities}.")
        except ValueError:
            print("Error: Please enter a valid integer.")
    
    print("\nNow select additional cities for your tour (at least 2 cities).")
    print("Enter 'q' when you're done selecting cities.")
    
    selected_cities = []
    while True:
        try:
            city_input = input(f"Enter city index (1-{num_cities}, excluding {start_city+1}) or 'q' to finish: ")
            
            if city_input.lower() == 'q':
                if len(selected_cities) >= 2:
                    break
                else:
                    print("Error: You must select at least 2 additional cities.")
                    continue
            
            city_idx = int(city_input) - 1
            

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
            city_input = ""
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
    start_city = np.random.randint(0, num_cities)
    print(f"Randomly selected {cities_names[start_city]} as the starting city.")

    all_cities_except_start = list(range(num_cities))
    all_cities_except_start.remove(start_city)

    num_cities_to_select = np.random.randint(8, num_cities)

    selected_cities = np.random.choice(
        all_cities_except_start, 
        size=min(num_cities_to_select, len(all_cities_except_start)), 
        replace=False
    ).tolist()
    
    return start_city, selected_cities


def display_tour_cities(tour, cities_names, is_interactive=False, initial_length=None):
    selected_city_names = [cities_names[i] for i in tour[1:]]

    city_mode = "Selected" if is_interactive else "Randomly selected"
    print(f"{city_mode} {len(selected_city_names)} cities to visit:")

    cities_per_row = 4
    for i in range(0, len(selected_city_names), cities_per_row):
        row_cities = selected_city_names[i:i+cities_per_row]
        formatted_cities = ", ".join(row_cities)
        print(f"  {formatted_cities}")

    if initial_length is not None:
        print(f"Initial Tour Distance: {initial_length:.2f}")


def create_initial_tour(distance_matrix, cities_names, num_cities, interactive_mode):
    print("\nGenerating nearest neighbor tour...")
    
    if interactive_mode:
        start_city, selected_cities = select_cities_interactively(cities_names, num_cities)
    else:
        start_city, selected_cities = select_cities_randomly(cities_names, num_cities)
    
    tour = nearest_neighbor_tour(distance_matrix, start_city, selected_cities)
    initial_length = calculate_tour_length(tour, distance_matrix)

    display_tour_cities(tour, cities_names, is_interactive=interactive_mode, initial_length=initial_length)
    
    return tour, initial_length, start_city
