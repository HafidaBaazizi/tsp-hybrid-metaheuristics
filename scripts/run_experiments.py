
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse
import csv
from pathlib import Path
from statistics import mean

from src.tsp_instance import load_tsp_instance
from src.nearest_neighbor import nearest_neighbor
from src.memetic_ga import memetic_algorithm
from src.tsplib_solutions import load_best_known_solutions
from src.utils import relative_gain_percent

def gap_percent(cost: float, optimum: int | None) -> float:
    if optimum is None or optimum == 0:
        return float('nan')
    return 100.0 * (cost - optimum) / optimum

def main() -> None:
    parser = argparse.ArgumentParser(description='Run TSP experiments on TSPLIB instances.')
    parser.add_argument('--data-dir', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--runs', type=int, default=2)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--solutions', default='data/tsplib/solutions.txt')
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    histories_dir = output_path.parent / 'histories'
    histories_dir.mkdir(parents=True, exist_ok=True)

    solutions = load_best_known_solutions(args.solutions) if Path(args.solutions).exists() else {}
    tsp_files = sorted([p for p in data_dir.glob('*.tsp')])

    rows = []
    for tsp_file in tsp_files:
        instance = load_tsp_instance(tsp_file)
        optimum = solutions.get(instance.name)
        greedy = nearest_neighbor(instance.distance_matrix, start=0)
        greedy_gap = gap_percent(greedy['cost'], optimum)

        print(f"\nInstance {instance.name} (n={instance.dimension})")
        print(f"  Glouton : cout={greedy['cost']} | temps={greedy['time']:.4f}s")

        meta_costs, meta_times = [], []
        for run in range(1, args.runs + 1):
            result = memetic_algorithm(instance.distance_matrix, seed=args.seed + run)
            meta_costs.append(result['cost'])
            meta_times.append(result['time'])
            meta_gap = gap_percent(result['cost'], optimum)
            gain = relative_gain_percent(greedy['cost'], result['cost'])
            rows.append({
                'instance': instance.name,
                'dimension': instance.dimension,
                'run': run,
                'best_known': optimum,
                'greedy_cost': greedy['cost'],
                'greedy_time_s': round(greedy['time'], 6),
                'greedy_gap_pct': round(greedy_gap, 4) if greedy_gap == greedy_gap else '',
                'meta_cost': result['cost'],
                'meta_time_s': round(result['time'], 6),
                'meta_gap_pct': round(meta_gap, 4) if meta_gap == meta_gap else '',
                'gain_pct': round(gain, 4),
            })
            print(f"  Run {run}: memetique={result['cost']} | temps={result['time']:.4f}s | gain={gain:.2f}%")
            history_path = histories_dir / f"{instance.name}_run{run}_history.csv"
            with history_path.open('w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['generation', 'best_cost'])
                for gen, cost in enumerate(result['history']):
                    writer.writerow([gen, cost])

    with output_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nResultats detailles enregistres dans : {output_path}")

if __name__ == '__main__':
    main()
