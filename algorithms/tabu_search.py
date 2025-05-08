"""
Tabu Search implementation for the Traveling Salesman Problem.

This module provides a Tabu Search algorithm to solve the TSP.
Tabu Search is a metaheuristic that guides a local search procedure
to explore the solution space beyond local optimality.
"""

import numpy as np
import random
import time
from core.distance import calculate_route_distance


class TabuSearch:
    """
    Tabu Search algorithm for solving the Traveling Salesman Problem.
    """
    
    def __init__(self, distance_matrix, tabu_tenure=10, max_iterations=100):
        """
        Initialize the Tabu Search algorithm.
        
        Args:
            distance_matrix (numpy.ndarray): Distance matrix between cities
            tabu_tenure (int): How long a move remains tabu (forbidden)
            max_iterations (int): Maximum number of iterations
        """
        self.distance_matrix = distance_matrix
        self.num_cities = distance_matrix.shape[0]
        self.tabu_tenure = tabu_tenure
        self.max_iterations = max_iterations
        
        # Initialize tabu list as a matrix
        self.tabu_list = np.zeros((self.num_cities, self.num_cities), dtype=int)
        
        # Performance tracking
        self.iterations = []
        self.distances = []
        self.best_distances = []
    
    def initialize_solution(self):
        """
        Create an initial solution by randomly ordering the cities.
        
        Returns:
            list: Initial random route
        """
        initial_solution = list(range(self.num_cities))
        random.shuffle(initial_solution)
        return initial_solution
    
    def evaluate_solution(self, solution):
        """
        Calculate the total distance of a route.
        
        Args:
            solution (list): List of city indices representing a route
            
        Returns:
            float: Total distance of the route
        """
        return calculate_route_distance(solution, self.distance_matrix)
    
    def get_best_neighbor(self, current_solution, current_iteration):
        """
        Find the best non-tabu neighbor by swapping pairs of cities.
        
        Args:
            current_solution (list): Current route
            current_iteration (int): Current iteration number
            
        Returns:
            tuple: (best_neighbor, move, best_distance) where move is (i, j)
        """
        best_neighbor = None
        best_distance = float('inf')
        best_move = None
        
        # Try swapping each pair of cities
        for i in range(self.num_cities - 1):
            for j in range(i + 1, self.num_cities):
                # Skip if the move is tabu and not meeting aspiration criteria
                if (self.tabu_list[i, j] > current_iteration and 
                    best_distance < float('inf')):
                    continue
                
                # Create a new solution by swapping cities i and j
                neighbor = current_solution.copy()
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                
                # Evaluate the neighbor
                distance = self.evaluate_solution(neighbor)
                
                # If this is the best neighbor so far, or the move is tabu but meets aspiration criteria
                if distance < best_distance:
                    best_neighbor = neighbor
                    best_distance = distance
                    best_move = (i, j)
        
        return best_neighbor, best_move, best_distance
    
    def update_tabu_list(self, move, current_iteration):
        """
        Update the tabu list after a move.
        
        Args:
            move (tuple): The move (i, j) that was made
            current_iteration (int): Current iteration number
        """
        i, j = move
        # The move is tabu for tabu_tenure iterations
        self.tabu_list[i, j] = current_iteration + self.tabu_tenure
        self.tabu_list[j, i] = current_iteration + self.tabu_tenure
    
    def solve(self, initial_solution=None, verbose=True):
        """
        Run the Tabu Search algorithm to solve the TSP.
        
        Args:
            initial_solution (list, optional): Initial route. If None, a random one is created.
            verbose (bool): Whether to print progress information
            
        Returns:
            tuple: (best_solution, best_distance)
        """
        # Initialize solution
        if initial_solution is None:
            current_solution = self.initialize_solution()
        else:
            current_solution = initial_solution.copy()
        
        current_distance = self.evaluate_solution(current_solution)
        
        # Best solution so far
        best_solution = current_solution.copy()
        best_distance = current_distance
        
        # Start timing
        start_time = time.time()
        
        # Clear performance tracking
        self.iterations = []
        self.distances = []
        self.best_distances = []
        
        # Main loop
        for iteration in range(self.max_iterations):
            # Get the best non-tabu neighbor
            neighbor, move, neighbor_distance = self.get_best_neighbor(current_solution, iteration)
            
            # Update current solution
            current_solution = neighbor
            current_distance = neighbor_distance
            
            # Update the tabu list
            self.update_tabu_list(move, iteration)
            
            # Update best solution if needed
            if current_distance < best_distance:
                best_solution = current_solution.copy()
                best_distance = current_distance
                if verbose:
                    print(f"Iteration {iteration}: New best distance = {best_distance:.2f}")
            
            # Track performance
            self.iterations.append(iteration)
            self.distances.append(current_distance)
            self.best_distances.append(best_distance)
            
            # Early stopping if no improvement for a long time
            if len(self.best_distances) > 20 and all(
                abs(self.best_distances[-1] - d) < 1e-6 for d in self.best_distances[-20:]
            ):
                if verbose:
                    print(f"Early stopping at iteration {iteration}: No improvement for 20 iterations")
                break
        
        # End timing
        end_time = time.time()
        
        if verbose:
            print(f"\nTabu Search completed in {end_time - start_time:.2f} seconds")
            print(f"Best distance: {best_distance:.2f}")
            print(f"Best solution: {best_solution}")
        
        return best_solution, best_distance


def solve_tsp(distance_matrix, tabu_tenure=10, max_iterations=100, verbose=True):
    """
    Convenience function to solve a TSP using Tabu Search.
    
    Args:
        distance_matrix (numpy.ndarray): Distance matrix between cities
        tabu_tenure (int): How long a move remains tabu
        max_iterations (int): Maximum number of iterations
        verbose (bool): Whether to print progress information
        
    Returns:
        tuple: (best_route, best_distance, tabu_search_object)
    """
    # Create and run the Tabu Search algorithm
    tabu_search = TabuSearch(
        distance_matrix=distance_matrix,
        tabu_tenure=tabu_tenure,
        max_iterations=max_iterations
    )
    
    best_route, best_distance = tabu_search.solve(verbose=verbose)
    
    return best_route, best_distance, tabu_search
