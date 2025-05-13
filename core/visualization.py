import matplotlib.pyplot as plt
import numpy as np

from core.tour import calculate_tour_length


def visualize_cities(cities_coordinates, cities_names=None, title="Moroccan Cities", 
                    route=None, start_city_idx=None):
    plt.figure(figsize=(14, 12))

    plt.axhspan(-20, 40, facecolor='lightskyblue', alpha=0.2, zorder=0)

    min_lon = min(cities_coordinates[:, 0]) - 0.7
    max_lon = max(cities_coordinates[:, 0]) + 0.9
    min_lat = min(cities_coordinates[:, 1]) - 0.7
    max_lat = max(cities_coordinates[:, 1]) + 0.7

    plt.fill_betweenx([min_lat, max_lat], min_lon - 5, min_lon, 
                     color='lightskyblue', alpha=0.2, zorder=0)

    if start_city_idx is not None and route is not None:

        non_start_mask = np.ones(len(cities_coordinates), dtype=bool)
        non_start_mask[start_city_idx] = False


        plt.scatter(cities_coordinates[non_start_mask, 0], cities_coordinates[non_start_mask, 1], 
                   c='red', s=150, edgecolor='black', zorder=3, alpha=0.7)


        plt.scatter(cities_coordinates[start_city_idx, 0], cities_coordinates[start_city_idx, 1], 
                   c='green', s=250, marker='*', edgecolor='black', linewidth=1.5, 
                   zorder=5, alpha=0.9)
    else:

        plt.scatter(cities_coordinates[:, 0], cities_coordinates[:, 1], c='red', s=150, edgecolor='black', zorder=3, alpha=0.7)

    for i, (x, y) in enumerate(cities_coordinates):
        label = cities_names[i] if cities_names else str(i)


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

    tour_length = None
    if route is not None:
        tour_length = calculate_tour_length(cities_coordinates, route)


        closed_route = route + [route[0]]


        route_x = [cities_coordinates[i, 0] for i in closed_route]
        route_y = [cities_coordinates[i, 1] for i in closed_route]


        for i in range(len(closed_route) - 1):

            curr_idx = closed_route[i]
            next_idx = closed_route[i + 1]
            x1, y1 = cities_coordinates[curr_idx]
            x2, y2 = cities_coordinates[next_idx]


            dx = x2 - x1
            dy = y2 - y1
            mid_x = x1 + dx * 0.6
            mid_y = y1 + dy * 0.6


            if start_city_idx is not None and curr_idx == start_city_idx:

                plt.plot([x1, x2], [y1, y2], 'g-', alpha=0.7, zorder=2.2, linewidth=2.0)


                plt.arrow(mid_x, mid_y, dx * 0.05, dy * 0.05,
                          head_width=0.09, head_length=0.11,
                          fc='green', ec='darkgreen', zorder=2.5, alpha=0.85,
                          length_includes_head=True)
            else:

                plt.plot([x1, x2], [y1, y2], 'b-', alpha=0.6, zorder=2, linewidth=1.5)


                plt.arrow(mid_x, mid_y, dx * 0.05, dy * 0.05,
                          head_width=0.08, head_length=0.1,
                          fc='blue', ec='blue', zorder=2, alpha=0.8,
                          length_includes_head=True)

    plt.title(title, fontsize=16, fontweight='bold', pad=10)

    plt.xlabel("Longitude (°)", fontsize=12)
    plt.ylabel("Latitude (°)", fontsize=12)

    plt.grid(True, linestyle='--', alpha=0.4)

    plt.xlim(min_lon, max_lon)
    plt.ylim(min_lat, max_lat)

    arrow_length = (max_lat - min_lat) * 0.05
    compass_x = min_lon + (max_lon - min_lon) * 0.05
    compass_y = max_lat - (max_lat - min_lat) * 0.07

    compass_circle = plt.Circle((compass_x, compass_y), arrow_length * 0.9,
                               fc='white', ec='lightgray', alpha=0.5, zorder=3)
    plt.gca().add_patch(compass_circle)

    plt.arrow(compass_x, compass_y - arrow_length/2, 0, arrow_length,
              head_width=0.1, head_length=0.1,
              fc='black', ec='black', zorder=4,
              length_includes_head=True, width=0.02)

    plt.text(compass_x, compass_y + arrow_length/2 + 0.05, 'N',
             fontsize=10, ha='center', va='center', fontweight='bold', zorder=4)

    plt.text(compass_x, compass_y + arrow_length/2 + 0.05, 'N',
             fontsize=10, ha='center', va='center', fontweight='bold', zorder=4)

    if route is not None:
        info_x = compass_x + (max_lon - min_lon) * 0.05
        info_y = compass_y


        route_info = (f"Starting City: {cities_names[start_city_idx]}"
                      f"\nVisited Cities: {len(route)}"
                      f"\nTour Length: {tour_length:.2f} units")
        plt.text(info_x, info_y, route_info,
                 fontsize=10, ha='left', va='center',
                 bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="gray", alpha=0.7),
                 zorder=4)

    plt.tight_layout(pad=2)

    try:
        plt.show()
    except Exception as e:
        print(f"Warning: Could not display plot ({str(e)}).")
        plt.close()


def visualize_results(cities_coordinates, cities_names, tour, optimized_tour, is_interactive):
    tour_mode = "User-Selected" if is_interactive else f"Random ({len(tour)} cities)"
    title = f"Moroccan Cities TSP - Tabu Search Optimized Tour ({tour_mode})"
    
    print(f"\nVisualizing Moroccan cities with optimized tour...")
    print("Displaying visualization. Close the window to exit.")
    
    visualize_cities(
        cities_coordinates=cities_coordinates,
        cities_names=cities_names,
        title=title,
        route=optimized_tour,
        start_city_idx=tour[0]
    )
