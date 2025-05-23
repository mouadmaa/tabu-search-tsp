"""
Module containing tabu search algorithm for the Traveling Salesman Problem.

This module provides functions to improve tours using tabu search with 2-opt moves.
"""

import time
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
                          (can be dynamically adjusted during search)
        """
        # Ensure tenure is an integer
        self.tenure = int(tenure)
        self.initial_tenure = int(tenure)  # Store initial value for potential reset
        self.tabu_list = deque()
    
    def reset_tenure(self):
        """Reset tabu tenure to its initial value."""
        self.tenure = int(self.initial_tenure)
    
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
        
        # Moves match if they involve the same indices
        # For 2-opt, we compare both ways since (i,j) and (j,i) represent the same move
        return (i1 == i2 and j1 == j2) or (i1 == j2 and j1 == i2)
    
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


def process_tabu_tenure(tabu_tenure_input, num_cities):
    """
    Process the tabu tenure parameter value based on input type and problem size.
    
    Args:
        tabu_tenure_input (str or int): The tabu tenure parameter value
        num_cities (int): The number of cities in the problem
        
    Returns:
        tuple: (int: processed tabu tenure value, str: description of the calculation)
    """
    import math
    
    if isinstance(tabu_tenure_input, str):
        if tabu_tenure_input.lower() == 'sqrt':
            tenure = int(round(math.sqrt(num_cities)))
            description = f"sqrt({num_cities}) = {tenure}"
        elif tabu_tenure_input.lower() == 'log':
            tenure = int(round(math.log(num_cities) * 3))
            description = f"log({num_cities}) * 3 = {tenure}"
        else:
            # Default fallback
            tenure = 10
            description = "default value = 10"
    else:
        # Use the provided integer value and ensure it's an integer
        try:
            tenure = int(tabu_tenure_input)
        except (ValueError, TypeError):
            # Fallback to default if conversion fails
            tenure = 10
            description = "default value = 10 (invalid input)"
        else:
            description = str(tenure)
    
    # Ensure a minimum tenure of 1
    tenure = max(1, tenure)
    
    return tenure, description


def tabu_search_optimization(tour, distance_matrix, tabu_tenure=10, max_iterations=1000, 
                             time_limit=60, aspiration_enabled=True, max_no_improvement=None,
                             intensification_threshold=20, diversification_threshold=50,
                             dynamic_tabu=False, progress_callback=None):
    """
    Improve a tour using tabu search with 2-opt moves.
    
    Args:
        tour (list): Initial tour to improve
        distance_matrix (numpy.ndarray): Matrix of distances between cities
        tabu_tenure (int or str): Number of iterations a move remains tabu, or a strategy like 'sqrt' or 'log'
        max_iterations (int): Maximum number of iterations
        time_limit (int): Maximum running time in seconds
        aspiration_enabled (bool): Whether to enable aspiration criteria (allow tabu moves if they improve the best solution)
        max_no_improvement (int): Stop after this many iterations without improvement. If None, uses tabu_tenure * 2
        intensification_threshold (int): Number of iterations without improvement before intensifying search
        diversification_threshold (int): Number of iterations without improvement before diversifying search
        dynamic_tabu (bool): Whether to dynamically adjust tabu tenure during search
        progress_callback (callable, optional): Function to call after each iteration with progress information
                                               Signature: callback(iteration, current_tour, current_length, 
                                                                  best_tour, best_length, move_info)
        
    Returns:
        tuple: (best_tour, best_tour_length, iterations, best_move_types)
    """
    start_time = time.time()
    num_cities = len(tour)
    
    # Process tabu tenure value - convert string strategies to actual integers
    tabu_tenure_value, description = process_tabu_tenure(tabu_tenure, num_cities)
    print(f"Using tabu tenure: {description}")
    
    # Initialize tabu list with the processed integer tenure
    tabu_list = TabuList(tenure=tabu_tenure_value)
    
    # Set max_no_improvement if not explicitly provided
    if max_no_improvement is None:
        max_no_improvement = tabu_tenure_value * 2
        print(f"Setting max iterations without improvement to: {max_no_improvement}")
    
    # Initialize current and best solutions
    current_tour = tour.copy()
    current_length = calculate_tour_length(current_tour, distance_matrix)
    
    best_tour = current_tour.copy()
    best_length = current_length
    
    iteration = 0
    improvements = 0
    best_move_types = {'2opt': 0}
    no_improvement_count = 0
    
    # No initial verbose output
    
    # Continue until we reach the maximum number of iterations or time limit
    while iteration < max_iterations and (time.time() - start_time) < time_limit:
        iteration += 1
        
        # Track the best move in the current neighborhood
        best_neighbor = None
        best_neighbor_length = float('inf')
        best_move_info = None
        
        # Generate and evaluate all possible 2-opt neighbors
        for neighbor, move_info in generate_2opt_neighbors(current_tour):
            neighbor_length = calculate_tour_length(neighbor, distance_matrix)
            
            # Check if the move is tabu
            is_tabu = tabu_list.is_tabu(move_info, iteration)
            
            # Apply aspiration criteria if enabled: allow tabu moves if they improve the best solution
            if not is_tabu or (aspiration_enabled and neighbor_length < best_length):
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
                best_move_types['2opt'] += 1
                improvements += 1
                no_improvement_count = 0
                
                # No verbose output for improvements
            else:
                no_improvement_count += 1
                
            # Call progress callback if provided
            if progress_callback:
                # Pass move_info properly
                move_info_type = best_move_info[0] if best_move_info else None
                progress_callback(iteration, current_tour, current_length, best_tour, best_length, best_move_info)
                
                # Track if this was an improvement move
                if current_length < best_length:
                    # This is tracked separately in best_move_types but we'll handle it in the callback
                    pass
        else:
            # If no valid move was found, we might be trapped in a local optimum
            
            # Option: could implement diversification strategies here (e.g., random perturbation)
            no_improvement_count += 1
        
        # Termination condition: if no improvement for a significant number of iterations
        if max_no_improvement is not None and no_improvement_count >= max_no_improvement:
            break
        
        # Handle intensification and diversification based on no improvement count
        if dynamic_tabu:
            if no_improvement_count >= diversification_threshold:
                # Increase tabu tenure temporarily to encourage diversification
                tabu_list.tenure = min(tabu_tenure_value * 2, tabu_tenure_value + 10)
            elif no_improvement_count >= intensification_threshold:
                # Decrease tabu tenure temporarily to encourage intensification
                tabu_list.tenure = max(3, tabu_tenure_value // 2)
            else:
                # Reset to normal tabu tenure
                tabu_list.tenure = tabu_tenure_value
    
    return best_tour, best_length, iteration, best_move_types
