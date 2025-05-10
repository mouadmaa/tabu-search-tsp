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
        self.move_counts = {'2opt': 0, 'swap': 0}
        self.move_types = []
    
    def start(self):
        """Start tracking performance."""
        self.start_time = time.time()
    
    def track_iteration(self, iteration, current_length, best_length, move_type=None):
        """
        Record performance metrics for current iteration.
        
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
        
        initial_length = self.tour_lengths[0]
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
            f"2-opt moves: {self.move_counts.get('2opt', 0)}\n"
            f"Swap moves: {self.move_counts.get('swap', 0)}"
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
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot tour lengths
        ax.plot(self.iterations, self.best_tour_lengths, 'r-', linewidth=2, 
                label='Best Tour Length')
        ax.plot(self.iterations, self.tour_lengths, 'b-', alpha=0.3, 
                label='Current Tour Length')
        
        # Calculate key metrics
        initial_length = self.tour_lengths[0]
        final_length = self.best_tour_lengths[-1]
        improvement = initial_length - final_length
        improvement_percentage = (improvement / initial_length) * 100
        
        # Add improvement rate info
        if len(self.best_tour_lengths) > 10:
            # Calculate improvements
            improvements = []
            for i in range(1, len(self.best_tour_lengths)):
                if self.best_tour_lengths[i] < self.best_tour_lengths[i-1]:
                    improvements.append(i)
            
            # Highlight improvement points
            if improvements:
                imp_iters = [self.iterations[i] for i in improvements]
                imp_lengths = [self.best_tour_lengths[i] for i in improvements]
                ax.scatter(imp_iters, imp_lengths, color='green', s=30, alpha=0.7, 
                           marker='o', label='Improvements')
        
        # Create enhanced stats box
        iterations_per_second = len(self.iterations) / self.times[-1] if self.times[-1] > 0 else 0
        stats = (
            f"Initial length: {initial_length:.1f}\n"
            f"Final length: {final_length:.1f}\n"
            f"Improvement: {improvement:.1f} ({improvement_percentage:.1f}%)\n"
            f"Total iterations: {len(self.iterations)}\n"
            f"Runtime: {self.times[-1]:.1f}s ({iterations_per_second:.1f} iter/s)\n"
            f"2-opt moves: {self.move_counts.get('2opt', 0)}\n"
            f"Swap moves: {self.move_counts.get('swap', 0)}"
        )
        
        # Add stats box to plot
        bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec="gray", alpha=0.8)
        ax.text(0.95, 0.95, stats, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', horizontalalignment='right', bbox=bbox_props)
        
        # Set labels and title
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Tour Length')
        ax.set_title(title or 'Tabu Search Performance')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper right')
        
        # Add a second x-axis for time
        if len(self.times) > 1:
            ax2 = ax.twiny()
            ax2.set_xlim(0, self.times[-1])
            ax2.set_xlabel('Time (seconds)')
            
            # Set reasonable number of ticks
            time_ticks = min(5, len(self.times))
            ax2.set_xticks(np.linspace(0, self.times[-1], time_ticks))
            ax2.set_xticklabels([f"{t:.1f}" for t in np.linspace(0, self.times[-1], time_ticks)])
        
        # Tight layout
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            plt.savefig(save_path)
            print(f"Performance report saved to {save_path}")
        
        return fig
