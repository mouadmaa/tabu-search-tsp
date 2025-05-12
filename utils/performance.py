"""
Performance tracking for TSP algorithms.

This module combines functionality for tracking performance metrics
of TSP optimization algorithms and displaying results.
"""

import os
import time
import matplotlib.pyplot as plt
import numpy as np


class PerformanceTracker:
    """
    Tracks performance metrics of optimization algorithms.
    """
    
    def __init__(self, initial_tour_length=None):
        """
        Initialize the performance tracker.
        
        Args:
            initial_tour_length (float, optional): The initial tour length
        """
        self.iterations = []
        self.times = []
        self.tour_lengths = []
        self.best_tour_lengths = []
        self.start_time = time.time()
        self.move_counts = {}
        self.initial_tour_length = initial_tour_length
    
    def track_iteration(self, iteration, current_tour_length, best_tour_length, move_info=None):
        """
        Track a single iteration's performance metrics.
        
        Args:
            iteration (int): The current iteration number
            current_tour_length (float): The current tour length
            best_tour_length (float): The best tour length found so far
            move_info (dict, optional): Information about the move performed
        """
        current_time = time.time() - self.start_time
        self.iterations.append(iteration)
        self.times.append(current_time)
        self.tour_lengths.append(current_tour_length)
        self.best_tour_lengths.append(best_tour_length)
        
        # Track move types
        if move_info and 'type' in move_info:
            move_type = move_info['type']
            self.move_counts[move_type] = self.move_counts.get(move_type, 0) + 1
    
    def plot_progress(self, show_plot=True, save_to_file=None):
        """
        Plot the optimization progress.
        
        Args:
            show_plot (bool): Whether to display the plot
            save_to_file (str, optional): File path to save the plot to
        """
        fig = self.show_report(save_path=save_to_file if save_to_file else None)
        if show_plot:
            plt.show()
        elif fig:
            plt.close(fig)
    
    def show_report(self, title=None, save_path=None):
        """
        Generate a simple performance visualization.
        
        Args:
            title: Optional title for the figure
            save_path: Optional path to save the figure
            
        Returns:
            The generated matplotlib figure
        """
        if not self.iterations:
            print("No performance data available.")
            return None
        
        # Create a figure with main plot and stats side by side
        fig = plt.figure(figsize=(12, 6))
    
        # Define grid layout with the main plot and stat box
        gs = fig.add_gridspec(1, 2, width_ratios=[3, 1])
    
        # Main plot
        ax_main = fig.add_subplot(gs[0, 0])
    
        # Calculate time in milliseconds
        times_ms = [t * 1000 for t in self.times]  # Convert seconds to milliseconds
    
        # Plot tour lengths in main plot
        ax_main.plot(self.iterations, self.best_tour_lengths, 'r-', linewidth=2,
                    label='Best Tour Length')
        ax_main.plot(self.iterations, self.tour_lengths, 'b-', alpha=0.3,
                    label='Current Tour Length')
    
        # Calculate key metrics
        initial_length = self.initial_tour_length if self.initial_tour_length is not None else self.tour_lengths[0]
        final_length = self.best_tour_lengths[-1]
        improvement = initial_length - final_length
        improvement_percentage = (improvement / initial_length) * 100
    
        # Add improvement rate info
        improvements = []
        if len(self.best_tour_lengths) > 10:
            # Calculate improvements
            for i in range(1, len(self.best_tour_lengths)):
                if self.best_tour_lengths[i] < self.best_tour_lengths[i-1]:
                    improvements.append(i)
    
            # Highlight improvement points
            if improvements:
                imp_iters = [self.iterations[i] for i in improvements]
                imp_lengths = [self.best_tour_lengths[i] for i in improvements]
                ax_main.scatter(imp_iters, imp_lengths, color='green', s=30, alpha=0.7,
                               marker='o', label='Improvements')
    
        # Create an enhanced stats box
        iterations_per_second = len(self.iterations) / self.times[-1] if self.times[-1] > 0 else 0
        stats = (
            f"Initial length      : {initial_length:.1f}\n\n"
            f"Final length        : {final_length:.1f}\n\n"
            f"Improvement     : {improvement:.1f} ({improvement_percentage:.1f}%)\n\n"
            f"Total iterations   : {len(self.iterations)}\n\n"
            f"Runtime             : {self.times[-1]*1000:.1f}ms ({iterations_per_second:.1f} iter/s)\n\n"
            f"2-opt moves       : {self.move_counts.get('2opt', 0)}"
        )
    
        # Set labels and title for the main plot
        ax_main.set_xlabel('Iterations')
        ax_main.set_ylabel('Tour Length')
        ax_main.set_title(title or 'Tabu Search Performance', pad=15, fontsize=14)
        ax_main.grid(True, linestyle='--', alpha=0.6)
        ax_main.legend(loc='upper right')
    
        # Add a second x-axis for time in milliseconds
        if len(self.times) > 1:
            ax2 = ax_main.twiny()
            ax2.set_xlim(0, self.times[-1])
            ax2.set_xlabel('Time (ms)')
    
            # Set a reasonable number of ticks
            time_ticks = min(5, len(times_ms))
            ax2.set_xticks(np.linspace(0, self.times[-1], time_ticks))
            ax2.set_xticklabels([f"{t:.1f}" for t in np.linspace(0, times_ms[-1], time_ticks)])
    
        # Create a stat box on the right
        ax_stats = fig.add_subplot(gs[0, 1])
        ax_stats.axis('off')  # Hide axes
        
        # Add performance stats to the right box
        ax_stats.text(0.1, 0.65, stats, transform=ax_stats.transAxes, fontsize=11,
                     verticalalignment='center', horizontalalignment='left')
        ax_stats.set_title('Performance Statistics', fontsize=12)
    
        # Tight layout
        plt.tight_layout(pad=1.5)
        
        # Save if a path provided
        if save_path:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            plt.savefig(save_path)
            print(f"Performance report saved to {save_path}")
        
        return fig


def create_performance_tracker(initial_tour_length=None):
    """
    Create and return a new performance tracker.
    
    Args:
        initial_tour_length (float, optional): The initial tour length
        
    Returns:
        PerformanceTracker: A new performance tracker
    """
    return PerformanceTracker(initial_tour_length)


def create_progress_callback(tracker, initial_tour_length=None):
    """
    Create a callback function for tracking progress.
    
    Args:
        tracker (PerformanceTracker): The performance tracker
        initial_tour_length (float, optional): The initial tour length
        
    Returns:
        callable: A callback function that can be passed to optimization algorithms
    """
    if initial_tour_length is not None:
        tracker.initial_tour_length = initial_tour_length
    
    def callback(iteration, current_tour, current_length, best_tour, best_length, move_info):
        # Extract move type from move_info if available
        move_type = None
        if move_info and isinstance(move_info, tuple) and len(move_info) > 0:
            move_type = {'type': move_info[0]}
        
        tracker.track_iteration(iteration, current_length, best_length, move_type)
    
    return callback


def display_performance_results(tracker, initial_length, optimized_length, iterations, move_types, optimization_time, args):
    """
    Display performance results in a user-friendly format.
    
    Args:
        tracker (PerformanceTracker): The performance tracker
        initial_length (float): Initial tour length
        optimized_length (float): Optimized tour length
        iterations (int): Number of iterations performed
        move_types (dict): Dictionary of move types and counts
        optimization_time (float): Total optimization time in seconds
        args (argparse.Namespace): Command line arguments
    """
    # Update tracker with the move types from the optimization
    if move_types and '2opt' in move_types:
        tracker.move_counts['2opt'] = move_types['2opt']
        
    # Calculate improvement metrics
    improvement = initial_length - optimized_length
    improvement_percentage = (improvement / initial_length) * 100
    
    # Create a combined tabu search summary including settings and performance
    print("\nTabu Search Optimization Summary:")
    print("-" * 50)
    print(f"Tour Length:     {initial_length:.2f} → {optimized_length:.2f}")
    print(f"Improvement:     {improvement:.2f} ({improvement_percentage:.2f}%)")
    print(f"Iterations:      {iterations}")
    print(f"Runtime:         {optimization_time:.2f} seconds")
    if iterations > 0 and optimization_time > 0:
        print(f"Speed:          {iterations/optimization_time:.2f} iterations/second")
    print(f"2-opt Moves:     {tracker.move_counts.get('2opt', 0)}")
    print("-" * 50)
    
    # Generate performance visualization if requested
    if hasattr(args, 'show_performance') and args.show_performance:
        print("\nGenerating performance visualization...")
        title = "Tabu Search Optimization Performance"
        tracker.show_report(title=title, save_path=args.save_performance if hasattr(args, 'save_performance') else None)
        plt.show()
    elif hasattr(args, 'save_performance') and args.save_performance:
        print(f"\nSaving performance data to {args.save_performance}...")
        title = "Tabu Search Optimization Performance"
        fig = tracker.show_report(title=title, save_path=args.save_performance)
        if fig:
            plt.close(fig)
