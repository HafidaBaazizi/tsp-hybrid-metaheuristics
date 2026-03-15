
from __future__ import annotations
from typing import List

def tour_cost(tour: List[int], distance_matrix: List[List[int]]) -> int:
    total = 0
    n = len(tour)
    for i in range(n):
        total += distance_matrix[tour[i]][tour[(i + 1) % n]]
    return int(total)

def is_valid_tour(tour: List[int], n: int) -> bool:
    return len(tour) == n and sorted(tour) == list(range(n))

def relative_gain_percent(reference_cost: float, candidate_cost: float) -> float:
    if reference_cost == 0:
        return 0.0
    return 100.0 * (reference_cost - candidate_cost) / reference_cost
