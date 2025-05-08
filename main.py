import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# For interactive display, you need tkinter installed.
# Install it on Ubuntu/Debian with: sudo apt-get install python3-tk
# Install it on CentOS/RHEL with: sudo yum install python3-tkinter
# Install it on Windows with: pip install tk

def generate_cities(num_cities, seed=None, x_range=(0, 100), y_range=(0, 100)):
    """
    Generate random city coordinates in a 2D plane.
    
    Args:
        num_cities (int): Number of cities to generate
        seed (int, optional): Random seed for reproducibility
        x_range (tuple): Range for x coordinates (min, max)
        y_range (tuple): Range for y coordinates (min, max)
        
    Returns:
        numpy.ndarray: Array of shape (num_cities, 2) with city coordinates
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate random coordinates
    x_coords = np.random.uniform(x_range[0], x_range[1], num_cities)
    y_coords = np.random.uniform(y_range[0], y_range[1], num_cities)
    
    # Combine into a single array
    cities = np.column_stack((x_coords, y_coords))
    
    return cities

def get_morocco_cities():
    """
    Returns a dictionary with major Moroccan cities and their simplified coordinates
    in a longitude/latitude-like format.
    
    Returns:
        dict: Dictionary mapping city names to (longitude, latitude) coordinate tuples
    """
    # Morocco longitude range: approximately -10 to -1
    # Morocco latitude range: approximately 30 to 36
    # Coordinates are simplified but proportionally resemble real positions
    morocco_cities = {
        "Tangier": (-5.8, 35.8),       # Northern city
        "Tetouan": (-5.4, 35.6),       # Northern city, east of Tangier
        "Chefchaouen": (-5.3, 35.2),   # Northern, in the Rif mountains
        "Rabat": (-6.8, 34.0),         # Capital, on the Atlantic coast
        "Casablanca": (-7.6, 33.6),    # Major city on the Atlantic coast
        "Fes": (-5.0, 34.0),           # Northeast inland
        "Meknes": (-5.5, 33.9),        # Near Fes
        "Oujda": (-1.9, 34.7),         # Far eastern city, near Algeria
        "Nador": (-2.9, 35.2),         # Northeastern coastal city
        "Marrakesh": (-8.0, 31.6),     # Central, inland city
        "Agadir": (-9.6, 30.4),        # Southwestern coastal city
        "Essaouira": (-9.8, 31.5),     # Western coastal city
        "Ouarzazate": (-6.9, 30.9),    # South central, gateway to the desert
        "El Jadida": (-8.5, 33.2),     # Western coastal city
        "Safi": (-9.2, 32.3),          # Western coastal city
        "Beni Mellal": (-6.4, 32.3),   # Central inland city
        "Taza": (-4.0, 34.2),          # Northeastern city
        "Ifrane": (-5.1, 33.5),        # Middle Atlas mountain town
        "Larache": (-6.2, 35.2),       # Northern coastal city
        "Kenitra": (-6.6, 34.3),       # Atlantic coastal city north of Rabat
        "Hoceima": (-3.9, 35.2)        # Northern coastal city on Mediterranean
    }
    return morocco_cities

def morocco_cities_to_array(cities_dict):
    """
    Converts the dictionary of Moroccan cities to a NumPy array format
    suitable for TSP algorithms, and returns a list of city names in the same order.
    
    Args:
        cities_dict (dict): Dictionary mapping city names to (x,y) coordinate tuples
        
    Returns:
        tuple: (numpy.ndarray of shape (num_cities, 2), list of city names)
    """
    city_names = list(cities_dict.keys())
    coordinates = np.array([cities_dict[name] for name in city_names])
    return coordinates, city_names

def compute_distance_matrix(cities):
    """
    Compute the Euclidean distance matrix between all pairs of cities.
    
    Args:
        cities (numpy.ndarray): Array of shape (num_cities, 2) with city coordinates
        
    Returns:
        numpy.ndarray: Distance matrix of shape (num_cities, num_cities)
    """
    num_cities = cities.shape[0]
    distance_matrix = np.zeros((num_cities, num_cities))
    
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                # Calculate Euclidean distance between cities i and j
                distance_matrix[i, j] = np.sqrt(
                    np.sum((cities[i] - cities[j]) ** 2)
                )
    
    return distance_matrix

def visualize_cities(cities, title="Traveling Salesman Problem: Morocco", save_to_file=False, filename="morocco_tsp.png", city_names=None):
    """
    Visualize the cities on a map-like display. Can display interactively or save to file.
    
    Args:
        cities (numpy.ndarray): Array of shape (num_cities, 2) with city coordinates
        title (str): Plot title
        save_to_file (bool): Whether to save the plot to a file instead of displaying
        filename (str): Filename to save the plot if save_to_file is True
        city_names (list, optional): List of city names corresponding to the coordinates
    """
    # Create a figure with more appropriate size
    plt.figure(figsize=(14, 12))
    
    # Create the scatter plot with enhanced styling
    plt.scatter(cities[:, 0], cities[:, 1], c='red', s=150, edgecolor='black', zorder=3, alpha=0.8)
    
    # Add city names with better styling and transparency
    for i, (x, y) in enumerate(cities):
        label = city_names[i] if city_names else str(i)
        plt.annotate(label, (x, y), 
                     xytext=(8, 8), 
                     textcoords='offset points', 
                     fontsize=11,
                     fontweight='bold',
                     alpha=0.7,  # Make the text slightly transparent
                     bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.6))  # More transparent background
    
    # Use a descriptive title with larger font size
    plt.title(title, fontsize=16, fontweight='bold', pad=10)
    
    # Change axis labels to longitude and latitude
    plt.xlabel("Longitude (°)", fontsize=12)
    plt.ylabel("Latitude (°)", fontsize=12)
    
    # Add a grid for better geographical reference
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add a light blue background to represent water/ocean
    plt.axhspan(-20, 40, facecolor='lightskyblue', alpha=0.3, zorder=0)
    
    # Calculate min and max coordinates to set appropriate limits with a modest margin
    min_lon = min(cities[:, 0]) - 0.7
    max_lon = max(cities[:, 0]) + 0.7
    min_lat = min(cities[:, 1]) - 0.7
    max_lat = max(cities[:, 1]) + 0.7
    
    # Set the axis limits to focus more on the cities
    plt.xlim(min_lon, max_lon)
    plt.ylim(min_lat, max_lat)
    
    # Add some contextual elements to make it look more like a map
    plt.fill_betweenx([min_lat, max_lat], min_lon - 5, min_lon, 
                     color='lightskyblue', alpha=0.5, zorder=0)
    
    # Add a simple north arrow in the top left corner
    arrow_length = (max_lat - min_lat) * 0.05  # Reduced size
    compass_x = min_lon + (max_lon - min_lon) * 0.08
    compass_y = max_lat - (max_lat - min_lat) * 0.15  # Position near top
    
    # Small white background circle
    compass_circle = plt.Circle((compass_x, compass_y), arrow_length * 0.6, 
                               fc='white', ec='lightgray', alpha=0.6, zorder=3)
    plt.gca().add_patch(compass_circle)
    
    # Simple north arrow
    plt.arrow(compass_x, compass_y - arrow_length/2, 0, arrow_length, 
              head_width=0.12, head_length=0.15, 
              fc='black', ec='black', zorder=4, 
              length_includes_head=True, width=0.02)
    
    # Small N label
    plt.text(compass_x, compass_y + arrow_length/2 + 0.05, 'N', 
             fontsize=10, ha='center', va='center', fontweight='bold', zorder=4)
    
    # Add more margin space around the entire plot
    plt.tight_layout(pad=2)

    if save_to_file:
        plt.savefig(filename)
        plt.close()
        print(f"City plot saved to {filename}")
    else:
        try:
            plt.show()
        except Exception as e:
            print(f"Warning: Could not display plot ({str(e)}). Saving to file instead.")
            plt.savefig(filename)
            plt.close()
            print(f"City plot saved to {filename}")

if __name__ == "__main__":
    # Use predefined Moroccan cities instead of random generation
    morocco_cities_dict = get_morocco_cities()
    cities, city_names = morocco_cities_to_array(morocco_cities_dict)

    print(f"Moroccan cities for TSP simulation ({len(city_names)} cities):")
    for i, name in enumerate(city_names):
        print(f"{i}: {name} at (longitude, latitude): {cities[i]}")

    # Compute distance matrix
    distance_matrix = compute_distance_matrix(cities)
    print("\nDistance Matrix (first 5x5 entries):")
    print(distance_matrix[:5, :5])

    print(f"\nDisplaying {len(city_names)} Moroccan cities for TSP...")
    # Try to display visualization interactively
    # If you encounter errors, set save_to_file=True
    visualize_cities(cities, title="Traveling Salesman Problem: Morocco",
                    save_to_file=False, city_names=city_names)

    # Example: To save to file instead of displaying, use:
    # visualize_cities(cities, save_to_file=True, filename="morocco_map.png", city_names=city_names)
