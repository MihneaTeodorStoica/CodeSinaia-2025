import math
import time
import os
import concurrent.futures
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats   # statistical tests

# Configuration: datasets 1 through 10
batch_size = 1000
file_paths = [f'_Data/output-Set{i}.txt' for i in range(1, 11)]
TYPE_MAP    = {211: 1, -211: -1}


def process_file(path: str) -> dict:
    """
    Reads a single file, computes paired t-test and two-sample ANOVA between
    π⁺ and π⁻ batch counts.
    """
    pos_batches, neg_batches = [], []
    count = 0

    with open(path, 'r') as f:
        batch_pos = batch_neg = 0
        for header in f:
            parts = header.split()
            if len(parts) != 2:
                continue
            n_particles = int(parts[1])
            ev_pos = ev_neg = 0
            for _ in range(n_particles):
                line = next(f, '')
                if not line:
                    break
                pdg = int(line.rsplit(' ', 1)[-1])
                if TYPE_MAP.get(pdg, 0) > 0:
                    ev_pos += 1
                elif TYPE_MAP.get(pdg, 0) < 0:
                    ev_neg += 1
            batch_pos += ev_pos
            batch_neg += ev_neg
            count += 1
            if count % batch_size == 0:
                pos_batches.append(batch_pos)
                neg_batches.append(batch_neg)
                batch_pos = batch_neg = 0

        # final partial batch
        if batch_pos or batch_neg:
            pos_batches.append(batch_pos)
            neg_batches.append(batch_neg)

    # paired t-test
    t_stat, t_pvalue = stats.ttest_rel(pos_batches, neg_batches)
    # two-sample ANOVA
    F_stat, F_pvalue = stats.f_oneway(pos_batches, neg_batches)
    return {
        't_stat': t_stat,
        't_pvalue': t_pvalue,
        'F_stat': F_stat,
        'F_pvalue': F_pvalue
    }


def plot_comparison(results: list[dict]):
    """
    Creates a single figure with two subplots:
      Top: ANOVA F-statistic (red) and p-value (blue) per file
      Bottom: Paired t-test t-statistic (red) and p-value (blue) per file
    Annotations (numbers) are black.
    """
    n = len(results)
    indices = np.arange(1, n+1)
    labels = [f"File {i}" for i in indices]

    F_stats = [r['F_stat']  for r in results]
    F_pvals = [r['F_pvalue'] for r in results]
    t_stats = [r['t_stat']  for r in results]
    t_pvals = [r['F_pvalue'] for r in results]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # ANOVA subplot
    ax1.plot(indices, F_stats, 'o-r', label='F-statistic')
    ax1.plot(indices, F_pvals, 's-b', label='p-value')
    ax1.set_ylabel('Value')
    ax1.set_title('ANOVA Results per File')
    for i, (fs, pv) in enumerate(zip(F_stats, F_pvals), start=1):
        ax1.text(i, fs + 0.02, f"{fs:.2f}", ha='center', va='bottom', fontsize=8, color='black')
        ax1.text(i, pv + 0.02, f"{pv:.3f}", ha='center', va='bottom', fontsize=8, color='black')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)

    # t-test subplot
    ax2.plot(indices, t_stats, 'o-r', label='t-statistic')
    ax2.plot(indices, t_pvals, 's-b', label='p-value')
    ax2.set_ylabel('Value')
    ax2.set_title('Paired t-test Results per File')
    for i, (ts, pv) in enumerate(zip(t_stats, t_pvals), start=1):
        ax2.text(i, ts + 0.1, f"{ts:.2f}", ha='center', va='bottom', fontsize=8, color='black')
        ax2.text(i, pv + 0.02, f"{pv:.3f}", ha='center', va='bottom', fontsize=8, color='black')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)

    ax2.set_xticks(indices)
    ax2.set_xticklabels(labels, rotation=45)

    plt.tight_layout()
    fname = 'stats_comparison.png'
    fig.savefig(fname)
    plt.close(fig)
    print(f"Saved combined plot: {fname}")


def main():
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count() or 1) as executor:
        results = list(executor.map(process_file, file_paths))

    plot_comparison(results)
    print(f"Total runtime: {time.perf_counter() - start:.3f}s")

if __name__ == '__main__':
    main()