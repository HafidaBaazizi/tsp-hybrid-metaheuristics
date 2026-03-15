
from __future__ import annotations
import random
import time
from typing import Dict, List, Tuple
from src.local_search import two_opt_first_improvement
from src.nearest_neighbor import nearest_neighbor_from_start
from src.utils import tour_cost

def ordered_crossover(parent1: List[int], parent2: List[int]) -> List[int]:
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b + 1] = parent1[a:b + 1]
    fill = [x for x in parent2 if x not in child]
    idx = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill[idx]
            idx += 1
    return child

def swap_mutation(tour: List[int]) -> List[int]:
    child = tour[:]
    i, j = sorted(random.sample(range(len(child)), 2))
    child[i], child[j] = child[j], child[i]
    return child

def inversion_mutation(tour: List[int]) -> List[int]:
    child = tour[:]
    i, j = sorted(random.sample(range(len(child)), 2))
    child[i:j+1] = reversed(child[i:j+1])
    return child

def tournament(population: List[List[int]], costs: List[int], k: int = 3) -> List[int]:
    idxs = random.sample(range(len(population)), k)
    best_idx = min(idxs, key=lambda idx: costs[idx])
    return population[best_idx][:]

def seeded_population(distance_matrix: List[List[int]], pop_size: int, rng: random.Random) -> List[List[int]]:
    n = len(distance_matrix)
    pop: List[List[int]] = []
    max_starts = min(8, n)
    chosen_starts = list(range(0, n, max(1, n // max_starts)))[:max_starts]
    for s in chosen_starts:
        pop.append(nearest_neighbor_from_start(distance_matrix, s)[0])
    while len(pop) < pop_size:
        t = list(range(n))
        rng.shuffle(t)
        pop.append(t)
    return pop[:pop_size]

def memetic_algorithm(
    distance_matrix: List[List[int]],
    seed: int = 42,
    pop_size: int = 28,
    generations: int = 90,
    crossover_rate: float = 0.9,
    mutation_rate: float = 0.18,
    elite_count: int = 2,
    local_search_rate: float = 0.35,
    stagnation_trigger: int = 15,
) -> Dict:
    rng = random.Random(seed)
    random.seed(seed)
    t0 = time.perf_counter()
    population = seeded_population(distance_matrix, pop_size, rng)
    costs = [tour_cost(t, distance_matrix) for t in population]
    best_idx = min(range(pop_size), key=lambda i: costs[i])
    best_tour = population[best_idx][:]
    best_cost = costs[best_idx]
    history = [best_cost]
    no_improve = 0

    for _ in range(generations):
        ranked = sorted(zip(population, costs), key=lambda x: x[1])
        population = [ind[:] for ind, _ in ranked]
        costs = [c for _, c in ranked]
        new_population = [population[i][:] for i in range(elite_count)]

        current_mut = mutation_rate * (2.0 if no_improve >= stagnation_trigger else 1.0)
        current_mut = min(current_mut, 0.45)

        while len(new_population) < pop_size:
            p1 = tournament(population, costs)
            p2 = tournament(population, costs)
            if rng.random() < crossover_rate:
                child = ordered_crossover(p1, p2)
            else:
                child = p1[:]

            if rng.random() < current_mut:
                if rng.random() < 0.5:
                    child = swap_mutation(child)
                else:
                    child = inversion_mutation(child)

            if rng.random() < local_search_rate:
                child, _ = two_opt_first_improvement(child, distance_matrix, max_passes=2)

            new_population.append(child)

        population = new_population
        costs = [tour_cost(t, distance_matrix) for t in population]
        gen_best_idx = min(range(pop_size), key=lambda i: costs[i])
        gen_best_cost = costs[gen_best_idx]

        if gen_best_cost < best_cost:
            best_cost = gen_best_cost
            best_tour = population[gen_best_idx][:]
            no_improve = 0
        else:
            no_improve += 1
        history.append(best_cost)

    elapsed = time.perf_counter() - t0
    return {'tour': best_tour, 'cost': int(best_cost), 'time': elapsed, 'history': history}
