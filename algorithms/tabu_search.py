import time
from collections import deque


def calculate_tour_length(tour, distance_matrix):
    tour_length = 0
    n = len(tour)
    
    for i in range(n - 1):
        tour_length += distance_matrix[tour[i], tour[i + 1]]
    
    tour_length += distance_matrix[tour[n - 1], tour[0]]
    
    return tour_length


def apply_2opt_move(tour, i, j):
    new_tour = tour.copy()

    new_tour[i+1:j+1] = reversed(tour[i+1:j+1])
    
    return new_tour


def generate_2opt_neighbors(tour):
    n = len(tour)
    neighbors = []
    
    for i in range(n - 2):
        for j in range(i + 2, n - 1):
            neighbor = apply_2opt_move(tour, i, j)
            neighbors.append((neighbor, ('2opt', i, j)))
    
    for i in range(n - 2):
        neighbor = apply_2opt_move(tour, i, n - 1)
        neighbors.append((neighbor, ('2opt', i, n - 1)))
    
    return neighbors


class TabuList:
    def __init__(self, tenure=10):
        self.tenure = int(tenure)
        self.initial_tenure = int(tenure)
        self.tabu_list = deque()
    
    def reset_tenure(self):
        self.tenure = int(self.initial_tenure)
    
    def add_move(self, move, current_iteration):
        expiration = current_iteration + self.tenure
        self.tabu_list.append((move, expiration))
    
    def is_tabu(self, move, current_iteration):
        self._clean_expired(current_iteration)

        for tabu_move, _ in self.tabu_list:
            if self._moves_match(move, tabu_move):
                return True
        
        return False

    def _moves_match(self, move1, move2):
        move_type1, i1, j1 = move1
        move_type2, i2, j2 = move2

        return (i1 == i2 and j1 == j2) or (i1 == j2 and j1 == i2)

    def _clean_expired(self, current_iteration):
        while self.tabu_list and self.tabu_list[0][1] <= current_iteration:
            self.tabu_list.popleft()
    
    def clear(self):
        self.tabu_list.clear()
    
    def __len__(self):
        return len(self.tabu_list)


def process_tabu_tenure(tabu_tenure_input, num_cities):
    import math
    
    if isinstance(tabu_tenure_input, str):
        if tabu_tenure_input.lower() == 'sqrt':
            tenure = int(round(math.sqrt(num_cities)))
            description = f"sqrt({num_cities}) = {tenure}"
        elif tabu_tenure_input.lower() == 'log':
            tenure = int(round(math.log(num_cities) * 3))
            description = f"log({num_cities}) * 3 = {tenure}"
        else:
            tenure = 10
            description = "default value = 10"
    else:
        try:
            tenure = int(tabu_tenure_input)
        except (ValueError, TypeError):
            tenure = 10
            description = "default value = 10 (invalid input)"
        else:
            description = str(tenure)

    tenure = max(1, tenure)
    
    return tenure, description


def tabu_search_optimization(tour, distance_matrix, tabu_tenure=10, max_iterations=1000, 
                             time_limit=60, aspiration_enabled=True, max_no_improvement=None,
                             intensification_threshold=20, diversification_threshold=50,
                             dynamic_tabu=False, progress_callback=None):

    start_time = time.time()
    num_cities = len(tour)

    tabu_tenure_value, description = process_tabu_tenure(tabu_tenure, num_cities)
    print(f"Using tabu tenure: {description}")

    tabu_list = TabuList(tenure=tabu_tenure_value)

    if max_no_improvement is None:
        max_no_improvement = tabu_tenure_value * 2
        print(f"Setting max iterations without improvement to: {max_no_improvement}")

    current_tour = tour.copy()
    current_length = calculate_tour_length(current_tour, distance_matrix)
    
    best_tour = current_tour.copy()
    best_length = current_length
    
    iteration = 0
    improvements = 0
    best_move_types = {'2opt': 0}
    no_improvement_count = 0


    while iteration < max_iterations and (time.time() - start_time) < time_limit:
        iteration += 1

        best_neighbor = None
        best_neighbor_length = float('inf')
        best_move_info = None

        for neighbor, move_info in generate_2opt_neighbors(current_tour):
            neighbor_length = calculate_tour_length(neighbor, distance_matrix)

            is_tabu = tabu_list.is_tabu(move_info, iteration)

            if not is_tabu or (aspiration_enabled and neighbor_length < best_length):
                if neighbor_length < best_neighbor_length:
                    best_neighbor_length = neighbor_length
                    best_neighbor = neighbor
                    best_move_info = move_info

        if best_neighbor is not None:
            current_tour = best_neighbor
            current_length = best_neighbor_length

            tabu_list.add_move(best_move_info, iteration)

            if current_length < best_length:
                best_tour = current_tour.copy()
                best_length = current_length
                best_move_types['2opt'] += 1
                improvements += 1
                no_improvement_count = 0

            else:
                no_improvement_count += 1

            if progress_callback:
                move_info_type = best_move_info[0] if best_move_info else None
                progress_callback(iteration, current_tour, current_length, best_tour, best_length, best_move_info)

                if current_length < best_length:
                    pass
        else:

            no_improvement_count += 1

        if max_no_improvement is not None and no_improvement_count >= max_no_improvement:
            break

        if dynamic_tabu:
            if no_improvement_count >= diversification_threshold:
                tabu_list.tenure = min(tabu_tenure_value * 2, tabu_tenure_value + 10)
            elif no_improvement_count >= intensification_threshold:
                tabu_list.tenure = max(3, tabu_tenure_value // 2)
            else:
                tabu_list.tenure = tabu_tenure_value
    
    return best_tour, best_length, iteration, best_move_types
