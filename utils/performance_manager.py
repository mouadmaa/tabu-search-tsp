"""
Performance management module for the Traveling Salesman Problem.

This module handles performance tracking and reporting for the TSP optimization process,
providing functions to create, manage, and display performance metrics.
"""

import time
import matplotlib.pyplot as plt
from utils.performance_tracker import PerformanceTracker


def create_performance_tracker():
    """
    Create and initialize a performance tracker.
    
    Returns:
        PerformanceTracker: Initialized performance tracker
    """
    tracker = PerformanceTracker()
    tracker.start()
    return tracker


def create_progress_callback(tracker, initial_tour_length=None):
    """
    Create a callback function for tracking optimization progress.
    
    Args:
        tracker (PerformanceTracker): The performance tracker to use
        initial_tour_length (float, optional): The initial tour length before optimization
        
    Returns:
        function: A callback function that updates the tracker
    """
    # Store the initial tour length in the tracker if provided
    if initial_tour_length is not None:
        tracker.set_initial_tour_length(initial_tour_length)
    
    def track_progress(iteration, current_tour, current_length, best_tour, best_length, move_info):
        move_type = move_info[0] if move_info else None
        tracker.track_iteration(iteration, current_length, best_length, move_type)
    
    return track_progress


def display_performance_results(tracker, initial_length, optimized_length, iterations, 
                              move_types, optimization_time, args):
    """
    Display performance results and generate visualizations if requested.
    
    Args:
        tracker (PerformanceTracker): The performance tracker with collected data
        initial_length (float): Initial tour length
        optimized_length (float): Optimized tour length after tabu search
        iterations (int): Number of iterations performed
        move_types (dict): Dictionary with count of different move types used
        optimization_time (float): Total optimization time in seconds
        args (Namespace): Command line arguments
    """
    # Calculate improvement metrics
    improvement = initial_length - optimized_length
    improvement_percentage = (improvement / initial_length) * 100
    
    # Create a simpler performance summary
    print("\nTabu Search Performance Summary:")
    print(f"Initial tour length: {initial_length:.2f}")
    print(f"Optimized tour length: {optimized_length:.2f}")
    print(f"Improvement: {improvement:.2f} ({improvement_percentage:.2f}%)")
    print(f"Iterations: {iterations}")
    print(f"Time: {optimization_time:.2f} seconds")
    if iterations > 0:
        print(f"Speed: {iterations/optimization_time:.2f} iterations/second")
    print(f"2-opt moves: {tracker.move_counts.get('2opt', 0)}")
    
    # Generate and display performance visualization if requested
    if args.show_performance or args.save_performance:
        import matplotlib.pyplot as plt
        title = "Tabu Search Performance for Morocco Cities"
        tracker.show_report(title=title, save_path=args.save_performance)
        
        if args.show_performance:
            plt.show()
