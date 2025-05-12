"""
Minimal performance tracking for Tabu Search Optimization.
"""

import os
import time
import matplotlib.pyplot as plt
import numpy as np


class PerformanceTracker:
    """Simplified performance tracking for tabu search optimization."""
    
    def __init__(self):
        """Initialize the performance tracker."""
        self.reset()
    
    def reset(self):
        """Reset all tracking data."""
        self.iterations = []
        self.tour_lengths = []
        self.best_tour_lengths = []
        self.times = []
        self.start_time = None
        self.move_counts = {'2opt': 0}
        self.move_types = []
        self.initial_tour_length = None
    
    def start(self):
        """Start tracking performance."""
        self.start_time = time.time()
    
    def set_initial_tour_length(self, initial_length):
        """Set the initial tour length before optimization."""
        self.initial_tour_length = initial_length
    
    def track_iteration(self, iteration, current_length, best_length, move_type=None):
        """
        Record performance metrics for the current iteration.
        
        Args:
            iteration: Current iteration number
            current_length: Length of the current tour
            best_length: Length of the best tour found so far
            move_type: Type of move applied ('2opt' or 'swap')
        """
        if self.start_time is None:
            self.start()
        
        self.iterations.append(iteration)
        self.tour_lengths.append(current_length)
        self.best_tour_lengths.append(best_length)
        self.times.append(time.time() - self.start_time)
        self.move_types.append(move_type)
        
        # Track move statistics
        if move_type:
            self.move_counts[move_type] = self.move_counts.get(move_type, 0) + 1
    
    def get_summary(self):
        """Return a summary of key performance metrics as a string."""
        if not self.iterations:
            return "No performance data available."
        
        # Use stored initial tour length if available, otherwise use first recorded length
        initial_length = self.initial_tour_length if self.initial_tour_length is not None else self.tour_lengths[0]
        final_length = self.best_tour_lengths[-1]
        improvement = initial_length - final_length
        improvement_percentage = (improvement / initial_length) * 100
        
        return (
            f"Performance Summary:\n"
            f"Initial tour length: {initial_length:.2f}\n"
            f"Final tour length: {final_length:.2f}\n"
            f"Improvement: {improvement:.2f} ({improvement_percentage:.2f}%)\n"
            f"Iterations: {len(self.iterations)}\n"
            f"Time: {self.times[-1]:.2f}s\n"
            f"2-opt moves: {self.move_counts.get('2opt', 0)}"
        )
    
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

        # Plot tour durations in main plot
        ax_main.plot(self.iterations, self.best_tour_lengths, 'r-', linewidth=2,
                    label='Best Tour Duration')
        ax_main.plot(self.iterations, self.tour_lengths, 'b-', alpha=0.3,
                    label='Current Tour Duration')

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
            f"Initial length    : {initial_length:.1f}\n\n"
            f"Final length      : {final_length:.1f}\n\n"
            f"Improvement    : {improvement:.1f} ({improvement_percentage:.1f}%)\n\n"
            f"Total iterations  : {len(self.iterations)}\n\n"
            f"Runtime            : {self.times[-1]*1000:.1f}ms ({iterations_per_second:.1f} iter/s)\n\n"
            f"2-opt moves     : {self.move_counts.get('2opt', 0)}"
        )

        # Set labels and title for the main plot
        ax_main.set_xlabel('Iterations')
        ax_main.set_ylabel('Tour Duration')
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
