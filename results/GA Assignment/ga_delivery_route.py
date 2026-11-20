"""
Artificial Intelligence - Individual Assignment
Genetic Algorithm for Delivery Route Optimisation

Student Name : Muhammad Adam bin Mohd Kamal @ Afdzal
Student ID   : 24006270
Course       : TEB2023 - Artificial Intelligence
"""

import random

# 1. Fictional Delivery Distance Matrix (in kilometres, symmetric)
# Depot is A; delivery locations are B, C, D, E, F, and G.
DISTANCE_MATRIX = {
    'A': {'A': 0, 'B': 4, 'C': 8, 'D': 6, 'E': 7, 'F': 9, 'G': 5},
    'B': {'A': 4, 'B': 0, 'C': 5, 'D': 7, 'E': 3, 'F': 8, 'G': 6},
    'C': {'A': 8, 'B': 5, 'C': 0, 'D': 4, 'E': 6, 'F': 3, 'G': 7},
    'D': {'A': 6, 'B': 7, 'C': 4, 'D': 0, 'E': 5, 'F': 6, 'G': 8},
    'E': {'A': 7, 'B': 3, 'C': 6, 'D': 5, 'E': 0, 'F': 4, 'G': 6},
    'F': {'A': 9, 'B': 8, 'C': 3, 'D': 6, 'E': 4, 'F': 0, 'G': 5},
    'G': {'A': 5, 'B': 6, 'C': 7, 'D': 8, 'E': 6, 'F': 5, 'G': 0},
}

DEPOT = 'A'
DELIVERY_LOCATIONS = ['B', 'C', 'D', 'E', 'F', 'G']


# 2. Fitness Function: Total Closed-Route Distance (Minimisation)
def calculate_route_distance(chromosome):
    """
    Calculates the total travel distance (in km) for a candidate route,
    starting at depot A, visiting each location once, and returning to depot A.
    """
    full_route = [DEPOT] + chromosome + [DEPOT]
    total_distance = 0
    for i in range(len(full_route) - 1):
        current_stop = full_route[i]
        next_stop = full_route[i + 1]
        total_distance += DISTANCE_MATRIX[current_stop][next_stop]
    return total_distance


# 3. Initial Population Generation
def create_initial_population(pop_size, locations):
    """
    Creates an initial population of valid random route permutations.
    Each delivery location (B-G) appears exactly once per chromosome.
    """
    population = []
    for _ in range(pop_size):
        route = locations[:]
        random.shuffle(route)
        population.append(route)
    return population


# 4. Parent Selection: Tournament Selection
def tournament_selection(population, fitness_scores, tournament_size=3):
    """
    Randomly samples k candidate routes and returns a copy of the one
    with the shortest total travel distance.
    """
    candidate_indices = random.sample(range(len(population)), tournament_size)
    best_index = min(candidate_indices, key=lambda idx: fitness_scores[idx])
    return population[best_index][:]


# 5. Route-Preserving Crossover: Order Crossover (OX1)
def order_crossover(parent1, parent2):
    """
    Combines two parent routes into a valid child route without duplicating
    or omitting any delivery location.
    """
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    # Copy a contiguous sub-route from parent1 into the child
    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]

    # Fill remaining positions using unused locations from parent2 in order
    remaining_genes = [gene for gene in parent2 if gene not in child]
    fill_idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = remaining_genes[fill_idx]
            fill_idx += 1

    return child


# 6. Mutation: Swap Mutation
def swap_mutation(chromosome, mutation_rate=0.15):
    """
    Applies a small random perturbation by swapping two delivery locations
    in the route with probability equal to mutation_rate.
    """
    mutated = chromosome[:]
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(mutated)), 2)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated


# 7. Main Genetic Algorithm Execution Loop
def run_genetic_algorithm(
    pop_size=40,
    generations=80,
    tournament_size=3,
    mutation_rate=0.15,
    n_elites=2,
    seed=42,
):
    """
    Evolves a population of candidate delivery routes over a fixed number of
    generations to minimise total closed-route distance.
    """
    random.seed(seed)  # Fixed random seed so the experiment can be reproduced

    population = create_initial_population(pop_size, DELIVERY_LOCATIONS)
    best_chromosome = None
    best_distance = float('inf')

    for gen in range(1, generations + 1):
        # Evaluate total route distance for every chromosome in the population
        fitness_scores = [calculate_route_distance(ind) for ind in population]

        # Rank routes from shortest distance (best) to longest distance (worst)
        ranked = sorted(zip(fitness_scores, population), key=lambda pair: pair[0])
        gen_best_dist, gen_best_route = ranked[0]

        if gen_best_dist < best_distance:
            best_distance = gen_best_dist
            best_chromosome = gen_best_route[:]

        # Print progress at generation 1, every 20 generations, and the final generation
        if gen == 1 or gen % 20 == 0 or gen == generations:
            route_str = " -> ".join([DEPOT] + best_chromosome + [DEPOT])
            print(f"Generation {gen:02d} | Best Distance: {best_distance} km | Route: {route_str}")

        # Elitism: copy the top routes unchanged into the next generation
        next_population = [ind[:] for _, ind in ranked[:n_elites]]

        # Generate offspring using selection, route-preserving crossover, and mutation
        while len(next_population) < pop_size:
            parent1 = tournament_selection(population, fitness_scores, tournament_size)
            parent2 = tournament_selection(population, fitness_scores, tournament_size)
            child = order_crossover(parent1, parent2)
            child = swap_mutation(child, mutation_rate)
            next_population.append(child)

        population = next_population

    best_full_route = [DEPOT] + best_chromosome + [DEPOT]
    return best_full_route, best_distance


if __name__ == "__main__":
    optimal_route, shortest_distance = run_genetic_algorithm(
        pop_size=40,
        generations=80,
        tournament_size=3,
        mutation_rate=0.15,
        n_elites=2,
        seed=42,
    )

    print("\n--- Final Genetic Algorithm Result ---")
    print(f"Best Delivery Route : {' -> '.join(optimal_route)}")
    print(f"Total Route Distance: {shortest_distance} km")
