"""
Module containing tabu search algorithm for the Traveling Salesman Problem.

This module provides functions to improve tours using tabu search with 2-opt and city swap moves.
"""

import time
import numpy as np
from collections import deque


def calculate_tour_length(tour, distance_matrix):
    """
    Calculate the total length of a tour.
    
    Args:
        tour (list): The tour to evaluate
        distance_matrix (numpy.ndarray): Matrix of distances between cities
        
    Returns:
        float: The total length of the tour
    """
    tour_length = 0
    n = len(tour)
    
    # Sum the distances between consecutive cities in the tour
    for i in range(n - 1):
        tour_length += distance_matrix[tour[i], tour[i + 1]]
    
    # Add the distance from the last city back to the first city
    tour_length += distance_matrix[tour[n - 1], tour[0]]
    
    return tour_length


def apply_2opt_move(tour, i, j):
    """
    Apply a 2-opt move to a tour by reversing the segment between positions i and j.
    
    Args:
        tour (list): The current tour
        i (int): Position of the first edge to remove
        j (int): Position of the second edge to remove
        
    Returns:
        list: A new tour after applying the 2-opt move
    """
    # Create a new tour to avoid modifying the original
    new_tour = tour.copy()
    
    # Reverse the segment between positions i and j
    # Note: we increment i by 1 because we're removing the edge between i and i+1
    new_tour[i+1:j+1] = reversed(tour[i+1:j+1])
    
    return new_tour


def apply_city_swap(tour, i, j):
    """
    Apply a city swap move by exchanging the positions of two cities in the tour.
    
    Args:
        tour (list): The current tour
        i (int): Position of the first city
        j (int): Position of the second city
        
    Returns:
        list: A new tour after swapping the cities
    """
    # Create a new tour to avoid modifying the original
    new_tour = tour.copy()
    
    # Swap the cities at positions i and j
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    
    return new_tour


def generate_2opt_neighbors(tour):
    """
    Generate all possible 2-opt neighbors for a given tour.
    
    Args:
        tour (list): The current tour
        
    Returns:
        list: A list of all possible 2-opt neighbor tours
    """
    n = len(tour)
    neighbors = []
    
    # Loop through all possible pairs of edges
    for i in range(n - 2):
        for j in range(i + 2, n - 1):
            # Apply the 2-opt move and add the resulting tour to the neighbors list
            neighbor = apply_2opt_move(tour, i, j)
            neighbors.append((neighbor, ('2opt', i, j)))
    
    # Also consider the edge between the last and first city
    for i in range(n - 2):
        # Apply the 2-opt move between edge i and the last edge
        neighbor = apply_2opt_move(tour, i, n - 1)
        neighbors.append((neighbor, ('2opt', i, n - 1)))
    
    return neighbors


def generate_swap_neighbors(tour):
    """
    Generate all possible city swap neighbors for a given tour.
    
    Args:
        tour (list): The current tour
        
    Returns:
        list: A list of all possible city swap neighbor tours
    """
    n = len(tour)
    neighbors = []
    
    # Loop through all possible pairs of cities
    for i in range(n):
        for j in range(i + 1, n):
            # Apply the city swap and add the resulting tour to the neighbors list
            neighbor = apply_city_swap(tour, i, j)
            neighbors.append((neighbor, ('swap', i, j)))
            
    return neighbors


class TabuList:
    """
    A data structure to maintain a list of tabu moves.
    
    Attributes:
        tenure (int): Number of iterations a move remains tabu
        tabu_list (deque): Queue containing tabu moves and their expiration iteration
    """
    
    def __init__(self, tenure=10):
        """
        Initialize a tabu list with a specified tenure.
        
        Args:
            tenure (int): Number of iterations a move remains tabu
        """
        self.tenure = tenure
        self.tabu_list = deque()
    
    def add_move(self, move, current_iteration):
        """
        Add a move to the tabu list.
        
        Args:
            move (tuple): Move attributes (move_type, index1, index2)
            current_iteration (int): Current iteration number
        """
        # Calculate the expiration iteration
        expiration = current_iteration + self.tenure
        self.tabu_list.append((move, expiration))
    
    def is_tabu(self, move, current_iteration):
        """
        Check if a move is currently tabu.
        
        Args:
            move (tuple): Move attributes (move_type, index1, index2)
            current_iteration (int): Current iteration number
            
        Returns:
            bool: True if the move is tabu, False otherwise
        """
        # Clean up expired tabu moves
        self._clean_expired(current_iteration)
        
        # Check if the move is in the tabu list
        for tabu_move, _ in self.tabu_list:
            if self._moves_match(move, tabu_move):
                return True
        
        return False
    
    def _moves_match(self, move1, move2):
        """
        Compare two moves to determine if they match.
        
        Args:
            move1 (tuple): First move attributes (move_type, index1, index2)
            move2 (tuple): Second move attributes (move_type, index1, index2)
            
        Returns:
            bool: True if the moves match, False otherwise
        """
        # Extract move components
        move_type1, i1, j1 = move1
        move_type2, i2, j2 = move2
        
        # Moves match if they have the same type and involve the same indices
        # For 2-opt, we compare both ways since (i,j) and (j,i) represent the same move
        if move_type1 == move_type2:
            if move_type1 == '2opt':
                return (i1 == i2 and j1 == j2) or (i1 == j2 and j1 == i2)
            else:  # 'swap'
                return (i1 == i2 and j1 == j2) or (i1 == j2 and j1 == i2)
        
        return False
    
    def _clean_expired(self, current_iteration):
        """
        Remove expired tabu moves from the list.
        
        Args:
            current_iteration (int): Current iteration number
        """
        while self.tabu_list and self.tabu_list[0][1] <= current_iteration:
            self.tabu_list.popleft()
    
    def clear(self):
        """Clear the tabu list."""
        self.tabu_list.clear()
    
    def __len__(self):
        """Return the number of tabu moves currently in the list."""
        return len(self.tabu_list)


def tabu_search_optimization(tour, distance_matrix, tabu_tenure=10, max_iterations=1000, 
                             time_limit=60, use_swap=True, prioritize_2opt=True, 
                             aspiration_enabled=True, verbose=False):
    """
    Improve a tour using tabu search with 2-opt moves and optionally city swaps.
    
    Args:
        tour (list): Initial tour to improve
        distance_matrix (numpy.ndarray): Matrix of distances between cities
        tabu_tenure (int): Number of iterations a move remains tabu
        max_iterations (int): Maximum number of iterations
        time_limit (int): Maximum running time in seconds
        use_swap (bool): Whether to use city swap operations
        prioritize_2opt (bool): Whether to prioritize 2-opt operations over city swaps
        aspiration_enabled (bool): Whether to enable aspiration criteria (allow tabu moves if they improve the best solution)
        verbose (bool): Whether to print progress information
        
    Returns:
        tuple: (best_tour, best_tour_length, iterations, best_move_types)
    """
    start_time = time.time()
    
    # Initialize tabu list
    tabu_list = TabuList(tenure=tabu_tenure)
    
    # Initialize current and best solutions
    current_tour = tour.copy()
    current_length = calculate_tour_length(current_tour, distance_matrix)
    
    best_tour = current_tour.copy()
    best_length = current_length
    
    iteration = 0
    improvements = 0
    best_move_types = {'2opt': 0, 'swap': 0}
    no_improvement_count = 0
    
    if verbose:
        print(f"Initial tour length: {current_length:.2f}")
        print(f"Tabu tenure: {tabu_tenure} iterations")
    
    # Continue until we reach the maximum number of iterations or time limit
    while iteration < max_iterations and (time.time() - start_time) < time_limit:
        iteration += 1
        
        # Track the best move in the current neighborhood
        best_neighbor = None
        best_neighbor_length = float('inf')
        best_move_info = None
        
        # Flag to track if we found a non-tabu move
        found_non_tabu_move = False
        
        # Generate and evaluate all possible 2-opt neighbors
        for neighbor, move_info in generate_2opt_neighbors(current_tour):
            neighbor_length = calculate_tour_length(neighbor, distance_matrix)
            
            # Check if the move is tabu
            is_tabu = tabu_list.is_tabu(move_info, iteration)
            
            # Apply aspiration criteria if enabled: allow tabu moves if they improve the best solution
            if not is_tabu or (aspiration_enabled and neighbor_length < best_length):
                found_non_tabu_move = True
                
                if neighbor_length < best_neighbor_length:
                    best_neighbor_length = neighbor_length
                    best_neighbor = neighbor
                    best_move_info = move_info
        
        # If no non-tabu move found with 2-opt and we're using city swaps, or if we don't prioritize 2-opt
        if (not found_non_tabu_move or not prioritize_2opt) and use_swap:
            for neighbor, move_info in generate_swap_neighbors(current_tour):
                neighbor_length = calculate_tour_length(neighbor, distance_matrix)
                
                # Check if the move is tabu
                is_tabu = tabu_list.is_tabu(move_info, iteration)
                
                # Apply aspiration criteria if enabled
                if not is_tabu or (aspiration_enabled and neighbor_length < best_length):
                    found_non_tabu_move = True
                    
                    if neighbor_length < best_neighbor_length:
                        best_neighbor_length = neighbor_length
                        best_neighbor = neighbor
                        best_move_info = move_info
        
        # If a valid move was found, update the current solution and add the move to the tabu list
        if best_neighbor is not None:
            current_tour = best_neighbor
            current_length = best_neighbor_length
            
            # Add the move to the tabu list
            tabu_list.add_move(best_move_info, iteration)
            
            # Update the best solution if improved
            if current_length < best_length:
                best_tour = current_tour.copy()
                best_length = current_length
                best_move_types[best_move_info[0]] += 1
                improvements += 1
                no_improvement_count = 0
                
                if verbose and (improvements % 10 == 0 or improvements == 1):
                    elapsed_time = time.time() - start_time
                    print(f"Iteration {iteration}: Best tour length = {best_length:.2f} "
                          f"(move type: {best_move_info[0]}), "
                          f"tabu list size: {len(tabu_list)}, "
                          f"elapsed time: {elapsed_time:.2f}s")
            else:
                no_improvement_count += 1
        else:
            # If no valid move was found, we might be trapped in a local optimum
            if verbose:
                print(f"Iteration {iteration}: No valid move found, may be trapped in local optimum.")
            
            # Option: could implement diversification strategies here (e.g., random perturbation)
            no_improvement_count += 1
        
        # Termination condition: if no improvement for a significant number of iterations
        if no_improvement_count >= max(50, tabu_tenure * 2):
            if verbose:
                print(f"Stopping: No improvement for {no_improvement_count} iterations.")
            break
    
    elapsed_time = time.time() - start_time
    
    if verbose:
        print(f"\nTabu search completed in {elapsed_time:.2f} seconds.")
        print(f"Iterations: {iteration}, Improvements: {improvements}")
        print(f"Move types used for improvements: 2-opt: {best_move_types['2opt']}, swap: {best_move_types['swap']}")
        print(f"Final best tour length: {best_length:.2f}")
    
    return best_tour, best_length, iteration, best_move_types
