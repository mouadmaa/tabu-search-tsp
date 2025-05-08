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

def visualize_cities(cities, title="City Locations", save_to_file=False, filename="cities_plot.png"):
    """
    Visualize the cities on a 2D plane. Can display interactively or save to file.
    
    Args:
        cities (numpy.ndarray): Array of shape (num_cities, 2) with city coordinates
        title (str): Plot title
        save_to_file (bool): Whether to save the plot to a file instead of displaying
        filename (str): Filename to save the plot if save_to_file is True
    """
    plt.figure(figsize=(10, 8))
    plt.scatter(cities[:, 0], cities[:, 1], c='red', s=100)
    
    # Add city indices
    for i, (x, y) in enumerate(cities):
        plt.annotate(str(i), (x, y), xytext=(5, 5), textcoords='offset points')
    
    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    
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
    # Set parameters
    num_cities = 20
    random_seed = 42
    
    # Generate random cities
    cities = generate_cities(num_cities, seed=random_seed)
    print(f"Generated {num_cities} cities:")
    print(cities)
    
    # Compute distance matrix
    distance_matrix = compute_distance_matrix(cities)
    print("\nDistance Matrix:")
    print(distance_matrix)
    
    # Try to display visualization interactively
    # If you encounter errors, set save_to_file=True
    visualize_cities(cities, save_to_file=False)
