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
    def __init__(self, initial_tour_length=None):
        self.iterations = []
        self.times = []
        self.tour_lengths = []
        self.best_tour_lengths = []
        self.start_time = time.time()
        self.move_counts = {}
        self.initial_tour_length = initial_tour_length
        self.start_city = None
        self.start_city_name = None
        self.num_visited_cities = None
        
    def set_tour_info(self, start_city, start_city_name, num_visited_cities):
        self.start_city = start_city
        self.start_city_name = start_city_name
        self.num_visited_cities = num_visited_cities
    
    def track_iteration(self, iteration, current_tour_length, best_tour_length, move_info=None):
        current_time = time.time() - self.start_time
        self.iterations.append(iteration)
        self.times.append(current_time)
        self.tour_lengths.append(current_tour_length)
        self.best_tour_lengths.append(best_tour_length)
        
        if move_info and 'type' in move_info:
            move_type = move_info['type']
            self.move_counts[move_type] = self.move_counts.get(move_type, 0) + 1
    
    def plot_progress(self, show_plot=True, save_to_file=None):
        fig = self.show_report(save_path=save_to_file if save_to_file else None)
        if show_plot:
            plt.show()
        elif fig:
            plt.close(fig)
    
    def show_report(self, title=None, save_path=None):
        if not self.iterations:
            print("No performance data available.")
            return None
        
        fig = plt.figure(figsize=(12, 6))
    
        gs = fig.add_gridspec(1, 2, width_ratios=[3, 1])
    
        ax_main = fig.add_subplot(gs[0, 0])
    
        times_ms = [t * 1000 for t in self.times]
    
        ax_main.plot(self.iterations, self.best_tour_lengths, 'r-', linewidth=2,
                    label='Best Tour Distance')
        ax_main.plot(self.iterations, self.tour_lengths, 'b-', alpha=0.3,
                    label='Current Tour Distance')
    
        initial_length = self.initial_tour_length if self.initial_tour_length is not None else self.tour_lengths[0]
        final_length = self.best_tour_lengths[-1]
        improvement = initial_length - final_length
        improvement_percentage = (improvement / initial_length) * 100
    
        improvements = []
        if len(self.best_tour_lengths) > 10:
            for i in range(1, len(self.best_tour_lengths)):
                if self.best_tour_lengths[i] < self.best_tour_lengths[i-1]:
                    improvements.append(i)
    
            if improvements:
                imp_iters = [self.iterations[i] for i in improvements]
                imp_lengths = [self.best_tour_lengths[i] for i in improvements]
                ax_main.scatter(imp_iters, imp_lengths, color='green', s=30, alpha=0.7,
                               marker='o', label='Improvements')
    
        iterations_per_second = len(self.iterations) / self.times[-1] if self.times[-1] > 0 else 0
        
        start_city_info = ""
        if hasattr(self, 'start_city') and hasattr(self, 'start_city_name') and self.start_city is not None:
            start_city_info = f"Starting city      : {self.start_city_name}\n\n"
        
        visited_cities_info = ""
        if hasattr(self, 'num_visited_cities') and self.num_visited_cities is not None:
            visited_cities_info = f"Visited cities      : {self.num_visited_cities}\n\n"
        
        stats = (
            f"{start_city_info}"
            f"{visited_cities_info}"
            f"Initial distance      : {initial_length:.1f}\n\n"
            f"Final distance        : {final_length:.1f}\n\n"
            f"Improvement     : {improvement:.1f} ({improvement_percentage:.1f}%)\n\n"
            f"Total iterations   : {len(self.iterations)}\n\n"
            f"Runtime              : {self.times[-1]*1000:.1f}ms ({iterations_per_second:.1f} iter/s)\n\n"
            f"2-opt moves       : {self.move_counts.get('2opt', 0)}"
        )
    
        ax_main.set_xlabel('Iterations')
        ax_main.set_ylabel('Tour Distance')
        ax_main.set_title(title or 'Tabu Search Performance', pad=15, fontsize=14)
        ax_main.grid(True, linestyle='--', alpha=0.6)
        ax_main.legend(loc='upper right')
    
        if len(self.times) > 1:
            ax2 = ax_main.twiny()
            ax2.set_xlim(0, self.times[-1])
            ax2.set_xlabel('Time (ms)')
    
            time_ticks = min(5, len(times_ms))
            ax2.set_xticks(np.linspace(0, self.times[-1], time_ticks))
            ax2.set_xticklabels([f"{t:.1f}" for t in np.linspace(0, times_ms[-1], time_ticks)])
    
        ax_stats = fig.add_subplot(gs[0, 1])
        ax_stats.axis('off')
        
        ax_stats.text(0.1, 0.65, stats, transform=ax_stats.transAxes, fontsize=11,
                     verticalalignment='center', horizontalalignment='left')
        ax_stats.set_title('Performance Statistics', fontsize=12)
    
        plt.tight_layout(pad=1.5)
        
        if save_path:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            plt.savefig(save_path)
            print(f"Performance report saved to {save_path}")
        
        return fig


def create_performance_tracker(initial_tour_length=None, tour=None, cities_names=None):
    tracker = PerformanceTracker(initial_tour_length)
    
    if tour is not None and cities_names is not None and len(tour) > 0:
        start_city = tour[0]
        start_city_name = cities_names[start_city]
        num_visited_cities = len(tour)
        tracker.set_tour_info(start_city, start_city_name, num_visited_cities)
        
    return tracker


def create_progress_callback(tracker, initial_tour_length=None):
    if initial_tour_length is not None:
        tracker.initial_tour_length = initial_tour_length
    
    def callback(iteration, current_tour, current_length, best_tour, best_length, move_info):
        move_type = None
        if move_info and isinstance(move_info, tuple) and len(move_info) > 0:
            move_type = {'type': move_info[0]}
        
        tracker.track_iteration(iteration, current_length, best_length, move_type)
    
    return callback


def optimize_tour(tour, distance_matrix, args, initial_length, cities_names=None):
    from algorithms.tabu_search import tabu_search_optimization
    
    print("\nApplying tabu search optimization...")
    start_time = time.time()
    
    tracker = create_performance_tracker(initial_tour_length=initial_length, tour=tour, cities_names=cities_names)
    progress_callback = create_progress_callback(tracker, initial_tour_length=initial_length)
    
    optimized_tour, optimized_length, iterations, move_types = tabu_search_optimization(
        tour=tour,
        distance_matrix=distance_matrix,
        tabu_tenure=args.tabu_tenure,
        max_iterations=args.max_iterations,
        time_limit=args.time_limit,
        max_no_improvement=args.max_no_improvement,
        progress_callback=progress_callback
    )
    
    optimization_time = time.time() - start_time
    print("Optimization completed.")
    
    display_performance_results(
        tracker, initial_length, optimized_length, 
        iterations, move_types, optimization_time, args
    )
    
    return optimized_tour, optimized_length


def display_performance_results(tracker, initial_length, optimized_length, iterations, move_types, optimization_time, args):
    if move_types and '2opt' in move_types:
        tracker.move_counts['2opt'] = move_types['2opt']
        
    improvement = initial_length - optimized_length
    improvement_percentage = (improvement / initial_length) * 100
    
    print("\nTabu Search Optimization Summary:")
    print("-" * 50)
    print(f"Tour Distance:     {initial_length:.2f} → {optimized_length:.2f}")
    print(f"Improvement:     {improvement:.2f} ({improvement_percentage:.2f}%)")
    print(f"Iterations:      {iterations}")
    print(f"Runtime:         {optimization_time:.2f} seconds")
    if iterations > 0 and optimization_time > 0:
        print(f"Speed:          {iterations/optimization_time:.2f} iterations/second")
    print(f"2-opt Moves:     {tracker.move_counts.get('2opt', 0)}")
    print("-" * 50)
    
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
