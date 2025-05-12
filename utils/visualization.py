"""
Visualization module for the Traveling Salesman Problem.

This module provides functions to visualize cities on a map.
"""

import matplotlib.pyplot as plt
import numpy as np

from core.tour import calculate_tour_length


def visualize_cities(cities_coordinates, cities_names=None, title="Moroccan Cities", 
                    route=None, start_city_idx=None):
    """
    Visualize the cities on a map-like display.
    
    Args:
        cities_coordinates (numpy.ndarray): Array of shape (num_cities, 2) with city coordinates
        cities_names (list, optional): List of city names corresponding to the coordinates
        title (str): Plot title
        route (list, optional): List of city indices representing a TSP route
        start_city_idx (int, optional): Index of the starting city to highlight
    """
    # Create a figure with the more appropriate size
    plt.figure(figsize=(14, 12))
    
    # Add a light blue background to represent water/ocean
    plt.axhspan(-20, 40, facecolor='lightskyblue', alpha=0.2, zorder=0)
    
    # Calculate min and max coordinates to set appropriate limits with a modest margin
    min_lon = min(cities_coordinates[:, 0]) - 0.7
    max_lon = max(cities_coordinates[:, 0]) + 0.9
    min_lat = min(cities_coordinates[:, 1]) - 0.7
    max_lat = max(cities_coordinates[:, 1]) + 0.7
    
    # Add some contextual elements to make it look more like a map
    plt.fill_betweenx([min_lat, max_lat], min_lon - 5, min_lon, 
                     color='lightskyblue', alpha=0.2, zorder=0)
    
    # Create markers for cities - if we have a starting city, we'll plot it separately
    if start_city_idx is not None and route is not None:
        # Create a mask for all cities except the starting city
        non_start_mask = np.ones(len(cities_coordinates), dtype=bool)
        non_start_mask[start_city_idx] = False
        
        # Plot regular cities first
        plt.scatter(cities_coordinates[non_start_mask, 0], cities_coordinates[non_start_mask, 1], 
                   c='red', s=150, edgecolor='black', zorder=3, alpha=0.7)

        # Plot the starting city with special styling (without a label to avoid legend)
        plt.scatter(cities_coordinates[start_city_idx, 0], cities_coordinates[start_city_idx, 1], 
                   c='green', s=250, marker='*', edgecolor='black', linewidth=1.5, 
                   zorder=5, alpha=0.9)
    else:
        # If no starting city specified, plot all cities normally
        plt.scatter(cities_coordinates[:, 0], cities_coordinates[:, 1], c='red', s=150, edgecolor='black', zorder=3, alpha=0.7)
    
    # Add city names with better styling and transparency
    for i, (x, y) in enumerate(cities_coordinates):
        label = cities_names[i] if cities_names else str(i)
        
        # Special styling for the starting city label
        if start_city_idx is not None and i == start_city_idx and route is not None:
            plt.annotate(label, (x, y), 
                         xytext=(8, 8), 
                         textcoords='offset points', 
                         fontsize=12,
                         fontweight='bold',
                         color='darkgreen',
                         alpha=0.9,
                         bbox=dict(boxstyle="round,pad=0.4", fc="lightgreen", ec="green", alpha=0.6))
        else:
            plt.annotate(label, (x, y), 
                         xytext=(8, 8), 
                         textcoords='offset points', 
                         fontsize=11,
                         fontweight='bold',
                         alpha=0.7,
                         bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.4))
    
    # Calculate tour length if a route is provided
    tour_length = None
    if route is not None:
        tour_length = calculate_tour_length(cities_coordinates, route)
        
        # Create a closed route by adding the starting city at the end
        closed_route = route + [route[0]]
        
        # Get coordinates for the route
        route_x = [cities_coordinates[i, 0] for i in closed_route]
        route_y = [cities_coordinates[i, 1] for i in closed_route]
        
        # Plot the route with arrows to show a direction
        for i in range(len(closed_route) - 1):
            # Current point and next point
            curr_idx = closed_route[i]
            next_idx = closed_route[i + 1]
            x1, y1 = cities_coordinates[curr_idx]
            x2, y2 = cities_coordinates[next_idx]
            
            # Calculate the midpoint for placing the arrow
            dx = x2 - x1
            dy = y2 - y1
            mid_x = x1 + dx * 0.6  # Position arrow at 60% along the line
            mid_y = y1 + dy * 0.6
            
            # Check if this is the edge starting from the starting city
            if start_city_idx is not None and curr_idx == start_city_idx:
                # Special styling for the line from starting city (green color, thicker)
                plt.plot([x1, x2], [y1, y2], 'g-', alpha=0.7, zorder=2.2, linewidth=2.0)
                
                # Special styling for the arrow from starting city (green)
                plt.arrow(mid_x, mid_y, dx * 0.05, dy * 0.05,
                          head_width=0.09, head_length=0.11,
                          fc='green', ec='darkgreen', zorder=2.5, alpha=0.85,
                          length_includes_head=True)
            else:
                # Regular styling for all other edges
                plt.plot([x1, x2], [y1, y2], 'b-', alpha=0.6, zorder=2, linewidth=1.5)
                
                # Regular styling for other arrows
                plt.arrow(mid_x, mid_y, dx * 0.05, dy * 0.05,
                          head_width=0.08, head_length=0.1,
                          fc='blue', ec='blue', zorder=2, alpha=0.8,
                          length_includes_head=True)

    # Use a descriptive title with a larger font size
    plt.title(title, fontsize=16, fontweight='bold', pad=10)

    # Change axis labels to longitude and latitude
    plt.xlabel("Longitude (°)", fontsize=12)
    plt.ylabel("Latitude (°)", fontsize=12)

    # Add a grid for better geographical reference
    plt.grid(True, linestyle='--', alpha=0.4)

    # Set the axis limits to focus more on the cities
    plt.xlim(min_lon, max_lon)
    plt.ylim(min_lat, max_lat)

    # Add a simple north arrow in the top left corner
    arrow_length = (max_lat - min_lat) * 0.05  # Reduced size
    compass_x = min_lon + (max_lon - min_lon) * 0.05  # Position near the left
    compass_y = max_lat - (max_lat - min_lat) * 0.06  # Position near the top

    # Small white background circle
    compass_circle = plt.Circle((compass_x, compass_y), arrow_length * 0.9,
                               fc='white', ec='lightgray', alpha=0.5, zorder=3)
    plt.gca().add_patch(compass_circle)

    # Simple north arrow
    plt.arrow(compass_x, compass_y - arrow_length/2, 0, arrow_length,
              head_width=0.1, head_length=0.1,
              fc='black', ec='black', zorder=4,
              length_includes_head=True, width=0.02)

    # Small N label
    plt.text(compass_x, compass_y + arrow_length/2 + 0.05, 'N',
             fontsize=10, ha='center', va='center', fontweight='bold', zorder=4)

    # Small N label
    plt.text(compass_x, compass_y + arrow_length/2 + 0.05, 'N',
             fontsize=10, ha='center', va='center', fontweight='bold', zorder=4)

    # Add route information next to the north arrow if available
    if route is not None:
        info_x = compass_x + (max_lon - min_lon) * 0.05  # Position to the right of compass
        info_y = compass_y

        # Add a route information box
        route_info = (f"Starting City: {cities_names[start_city_idx]}"
                      f"\nVisited Cities: {len(route)}"
                      f"\nTour Length: {tour_length:.2f} units")
        plt.text(info_x, info_y, route_info,
                 fontsize=10, ha='left', va='center',
                 bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="gray", alpha=0.7),
                 zorder=4)

    # Add more margin space around the entire plot
    plt.tight_layout(pad=2)

    # Display the plot
    try:
        plt.show()
    except Exception as e:
        print(f"Warning: Could not display plot ({str(e)}).")
        plt.close()
