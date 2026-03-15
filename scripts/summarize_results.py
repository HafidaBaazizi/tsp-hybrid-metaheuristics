from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def make_longtable(df: pd.DataFrame, out_path: Path) -> None:
    headers = ['Instance', 'n', 'BKS', 'Glouton', 'Gap G.(%)', 'Mem. meilleur', 'Gap M.(%)', 'Gain(%)', 'Temps M.(s)']
    lines = []
    lines.append(r'\begin{longtable}{lrrrrrrrr}')
    lines.append(r'\caption{Synthese des resultats experimentaux sur 22 instances TSPLIB.}\\')
    lines.append(r'\toprule')
    lines.append(' & '.join(headers) + r' \\')
    lines.append(r'\midrule')
    lines.append(r'\endfirsthead')
    lines.append(r'\toprule')
    lines.append(' & '.join(headers) + r' \\')
    lines.append(r'\midrule')
    lines.append(r'\endhead')
    for _, r in df.iterrows():
        vals = [
            r['instance'], int(r['dimension']),
            '-' if pd.isna(r['best_known']) else int(r['best_known']),
            int(r['greedy_cost']),
            '-' if pd.isna(r['greedy_gap_pct']) else f"{r['greedy_gap_pct']:.2f}",
            int(r['meta_best_cost']),
            '-' if pd.isna(r['meta_best_gap_pct']) else f"{r['meta_best_gap_pct']:.2f}",
            f"{r['gain_best_pct']:.2f}",
            f"{r['meta_time_mean_s']:.3f}",
        ]
        lines.append(' & '.join(map(str, vals)) + r' \\')
    lines.append(r'\bottomrule')
    lines.append(r'\end{longtable}')
    out_path.write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='Summarize experiment results and generate figures.')
    parser.add_argument('--input', required=True)
    parser.add_argument('--summary', required=True)
    parser.add_argument('--latex', required=True)
    parser.add_argument('--figure-dir', required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    summary_path = Path(args.summary)
    latex_path = Path(args.latex)
    fig_dir = Path(args.figure_dir)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    latex_path.parent.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    for c in ['best_known', 'greedy_gap_pct', 'meta_gap_pct', 'gain_pct']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    summary = df.groupby(['instance', 'dimension'], as_index=False).agg(
        best_known=('best_known', 'first'),
        greedy_cost=('greedy_cost', 'first'),
        greedy_time_s=('greedy_time_s', 'first'),
        greedy_gap_pct=('greedy_gap_pct', 'first'),
        meta_best_cost=('meta_cost', 'min'),
        meta_mean_cost=('meta_cost', 'mean'),
        meta_time_mean_s=('meta_time_s', 'mean'),
        gain_best_pct=('gain_pct', 'max'),
        gain_mean_pct=('gain_pct', 'mean'),
        meta_best_gap_pct=('meta_gap_pct', 'min'),
    ).sort_values('dimension')
    summary.to_csv(summary_path, index=False)
    make_longtable(summary, latex_path)

    g = summary.sort_values('gain_best_pct', ascending=False)
    plt.figure(figsize=(11, 8))
    plt.barh(g['instance'], g['gain_best_pct'])
    plt.gca().invert_yaxis()
    plt.xlabel('Gain relatif du meilleur run (%)')
    plt.ylabel('Instance')
    plt.title("Gain relatif de l'algorithme memetique par rapport au glouton")
    plt.tight_layout()
    plt.savefig(fig_dir / 'gain_by_instance.png', dpi=220)
    plt.close()

    c = summary.sort_values('dimension')
    plt.figure(figsize=(11, 6))
    plt.plot(c['dimension'], c['greedy_cost'], marker='o', label='Glouton')
    plt.plot(c['dimension'], c['meta_best_cost'], marker='s', label='Memetique (meilleur run)')
    plt.xlabel('Nombre de villes')
    plt.ylabel('Cout de la tournee')
    plt.title('Comparaison des couts selon la taille des instances')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / 'cost_comparison.png', dpi=220)
    plt.close()

    plt.figure(figsize=(11, 6))
    plt.plot(c['dimension'], c['greedy_time_s'], marker='o', label='Glouton')
    plt.plot(c['dimension'], c['meta_time_mean_s'], marker='s', label='Memetique')
    plt.yscale('log')
    plt.xlabel('Nombre de villes')
    plt.ylabel('Temps d execution (s, echelle logarithmique)')
    plt.title('Temps d execution des deux approches')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / 'time_comparison.png', dpi=220)
    plt.close()

    tmp = c.dropna(subset=['best_known'])
    plt.figure(figsize=(11, 6))
    plt.plot(tmp['dimension'], tmp['greedy_gap_pct'], marker='o', label='Gap glouton')
    plt.plot(tmp['dimension'], tmp['meta_best_gap_pct'], marker='s', label='Gap memetique')
    plt.xlabel('Nombre de villes')
    plt.ylabel('Ecart relatif au meilleur cout connu (%)')
    plt.title('Qualite des solutions par rapport aux meilleurs couts connus TSPLIB')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / 'gap_to_bks.png', dpi=220)
    plt.close()


if __name__ == '__main__':
    main()
