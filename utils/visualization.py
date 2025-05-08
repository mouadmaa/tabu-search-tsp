"""
Visualization module for the Traveling Salesman Problem.

This module provides functions to visualize cities on a map and
plot TSP routes/solutions in an informative and visually appealing way.
"""

import matplotlib.pyplot as plt
import numpy as np


def visualize_cities(cities, city_names=None, title="Traveling Salesman Problem: Morocco", 
                    save_to_file=False, filename="morocco_tsp.png", route=None):
    """
    Visualize the cities on a map-like display. Can display interactively or save to file.
    Optionally shows a TSP route connecting the cities.
    
    Args:
        cities (numpy.ndarray): Array of shape (num_cities, 2) with city coordinates
        city_names (list, optional): List of city names corresponding to the coordinates
        title (str): Plot title
        save_to_file (bool): Whether to save the plot to a file instead of displaying
        filename (str): Filename to save the plot if save_to_file is True
        route (list, optional): List of city indices representing a TSP route
    """
    # Create a figure with more appropriate size
    plt.figure(figsize=(14, 12))
    
    # Add a light blue background to represent water/ocean
    plt.axhspan(-20, 40, facecolor='lightskyblue', alpha=0.3, zorder=0)
    
    # Calculate min and max coordinates to set appropriate limits with a modest margin
    min_lon = min(cities[:, 0]) - 0.7
    max_lon = max(cities[:, 0]) + 0.7
    min_lat = min(cities[:, 1]) - 0.7
    max_lat = max(cities[:, 1]) + 0.7
    
    # Add some contextual elements to make it look more like a map
    plt.fill_betweenx([min_lat, max_lat], min_lon - 5, min_lon, 
                     color='lightskyblue', alpha=0.5, zorder=0)
    
    # If a route is provided, plot the route lines first (so cities appear on top)
    if route is not None:
        # Add the route as lines connecting the cities
        route_x = [cities[i, 0] for i in route]
        route_y = [cities[i, 1] for i in route]
        
        # Add the last connection back to the starting city to complete the tour
        route_x.append(route_x[0])
        route_y.append(route_y[0])
        
        # Plot the route
        plt.plot(route_x, route_y, 'g-', linewidth=1.5, alpha=0.8, zorder=2)
    
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
    
    # Set the axis limits to focus more on the cities
    plt.xlim(min_lon, max_lon)
    plt.ylim(min_lat, max_lat)
    
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


def plot_performance(iterations, distances, best_distances=None, title="TSP Optimization Progress"):
    """
    Plot the performance of the optimization algorithm over iterations.
    
    Args:
        iterations (list): List of iteration numbers
        distances (list): List of distances at each iteration
        best_distances (list, optional): List of best distances found so far at each iteration
        title (str): Plot title
    """
    plt.figure(figsize=(12, 6))
    
    # Plot the current solution distance at each iteration
    plt.plot(iterations, distances, 'b-', alpha=0.5, label='Current Solution')
    
    # If best distances are provided, plot them as well
    if best_distances:
        plt.plot(iterations, best_distances, 'r-', linewidth=2, label='Best Solution')
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Total Distance', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
