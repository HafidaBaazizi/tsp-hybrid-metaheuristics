
from __future__ import annotations
import time
from typing import Dict, List, Tuple
from src.utils import tour_cost

def nearest_neighbor_from_start(distance_matrix: List[List[int]], start: int) -> Tuple[List[int], int]:
    n = len(distance_matrix)
    unvisited = set(range(n))
    unvisited.remove(start)
    tour = [start]
    current = start
    while unvisited:
        nxt = min(unvisited, key=lambda city: distance_matrix[current][city])
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    return tour, tour_cost(tour, distance_matrix)

def nearest_neighbor(distance_matrix: List[List[int]], start: int = 0) -> Dict:
    t0 = time.perf_counter()
    tour, cost = nearest_neighbor_from_start(distance_matrix, start)
    elapsed = time.perf_counter() - t0
    return {'tour': tour, 'cost': cost, 'time': elapsed}

def best_nearest_neighbor(distance_matrix: List[List[int]], max_starts: int | None = None) -> Dict:
    n = len(distance_matrix)
    starts = list(range(n))
    if max_starts is not None and max_starts < n:
        # deterministic selection spread over the whole index range
        step = max(1, n // max_starts)
        starts = list(range(0, n, step))[:max_starts]
    t0 = time.perf_counter()
    best_tour, best_cost = None, None
    for s in starts:
        tour, cost = nearest_neighbor_from_start(distance_matrix, s)
        if best_cost is None or cost < best_cost:
            best_tour, best_cost = tour, cost
    elapsed = time.perf_counter() - t0
    return {'tour': best_tour, 'cost': best_cost, 'time': elapsed, 'starts_tested': len(starts)}
