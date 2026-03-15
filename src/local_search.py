
from __future__ import annotations
from typing import List, Tuple
from src.utils import tour_cost

def two_opt_first_improvement(tour: List[int], distance_matrix: List[List[int]], max_passes: int = 3) -> Tuple[List[int], int]:
    n = len(tour)
    best = tour[:]
    best_cost = tour_cost(best, distance_matrix)
    passes = 0
    improved = True
    while improved and passes < max_passes:
        improved = False
        passes += 1
        for i in range(1, n - 2):
            a, b = best[i - 1], best[i]
            for k in range(i + 1, n - 1):
                c, d = best[k], best[(k + 1) % n]
                delta = (distance_matrix[a][c] + distance_matrix[b][d]) - (distance_matrix[a][b] + distance_matrix[c][d])
                if delta < 0:
                    best[i:k + 1] = reversed(best[i:k + 1])
                    best_cost += delta
                    improved = True
                    break
            if improved:
                break
    return best, int(best_cost)
