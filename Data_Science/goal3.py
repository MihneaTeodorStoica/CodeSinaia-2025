import math
import time
import os
import concurrent.futures
import matplotlib.pyplot as plt
import numpy as np

# Configuration
batch_size = 1000          # Number of events per batch for memory-efficient processing
sigma_threshold = 3.0      # Significance threshold (σ units)
file_paths = [
    '_Data/output-Set0.txt',
    '_Data/output-Set1.txt',
    '_Data/output-Set2.txt',
    '_Data/output-Set3.txt',
    '_Data/output-Set4.txt',
    '_Data/output-Set5.txt',
    '_Data/output-Set6.txt',
    '_Data/output-Set7.txt',
    '_Data/output-Set8.txt',
    '_Data/output-Set9.txt',
    '_Data/output-Set10.txt',
]

# Pre-compile PDG lookup for O(1) mapping
TYPE_MAP = {211: 1, -211: -1}


def calculate_average_and_uncertainty(total_count: float, n_events: int) -> tuple[float, float]:
    if n_events <= 0:
        return float('nan'), float('nan')
    avg = total_count / n_events
    unc = math.sqrt(total_count) / n_events
    return avg, unc


def process_file(path: str) -> dict:
    """
    Process one data file, tally π⁺/π⁻ and record per-batch counts.
    Returns summary and batch-wise lists.
    """
    total_pos = total_neg = 0
    batch_pos = batch_neg = 0
    pos_batches, neg_batches = [], []
    event_count = 0
    start = time.perf_counter()

    with open(path, 'r') as f:
        readline = f.readline
        while True:
            header = readline()
            if not header:
                break
            parts = header.split()
            if len(parts) != 2:
                continue
            event_count += 1
            n_particles = int(parts[1])

            ev_pos = ev_neg = 0
            for _ in range(n_particles):
                line = readline()
                if not line:
                    break
                pdg = int(line.rsplit(' ', 1)[-1])
                typ = TYPE_MAP.get(pdg, 0)
                if typ > 0:
                    ev_pos += 1
                elif typ < 0:
                    ev_neg += 1

            total_pos += ev_pos
            total_neg += ev_neg
            batch_pos += ev_pos
            batch_neg += ev_neg

            if event_count % batch_size == 0:
                pos_batches.append(batch_pos)
                neg_batches.append(batch_neg)
                batch_pos = batch_neg = 0

    # capture any remaining batch
    if batch_pos or batch_neg:
        pos_batches.append(batch_pos)
        neg_batches.append(batch_neg)

    elapsed = time.perf_counter() - start
    avg_pos, unc_pos = calculate_average_and_uncertainty(total_pos, event_count)
    avg_neg, unc_neg = calculate_average_and_uncertainty(total_neg, event_count)
    diff = abs(total_pos - total_neg)
    combined_unc = math.hypot(unc_pos, unc_neg)
    sig = diff / combined_unc if combined_unc > 0 else float('inf')

    return {
        'file': path,
        'events': event_count,
        'total_pos': total_pos,
        'total_neg': total_neg,
        'avg_pos': avg_pos,
        'avg_neg': avg_neg,
        'unc_pos': unc_pos,
        'unc_neg': unc_neg,
        'diff': diff,
        'combined_unc': combined_unc,
        'significance': sig,
        'significant': sig > sigma_threshold,
        'time_s': elapsed,
        'pos_batches': pos_batches,
        'neg_batches': neg_batches
    }


def plot_batches(summary: dict) -> None:
    """
    Generate and save a plot of π⁺/π⁻ counts per batch for a file.
    """
    pos = summary['pos_batches']
    neg = summary['neg_batches']
    batches = np.arange(1, len(pos)+1) * batch_size
    fig, ax = plt.subplots()
    ax.plot(batches, pos, label='π⁺ per batch')
    ax.plot(batches, neg, label='π⁻ per batch')
    ax.set_xlabel('Events processed')
    ax.set_ylabel(f'Counts per {batch_size} events')
    ax.set_title(f"Batch counts for {os.path.basename(summary['file'])}")
    ax.legend()
    # annotate summary
    stats = (
        f"Events: {summary['events']}",
        f"Total π⁺={summary['total_pos']}, π⁻={summary['total_neg']}",
        f"Avg/event π⁺={summary['avg_pos']:.3f}±{summary['unc_pos']:.3f}",
        f"Avg/event π⁻={summary['avg_neg']:.3f}±{summary['unc_neg']:.3f}",
        f"Δ={summary['diff']}, Signif={summary['significance']:.2f}σ"
    )
    ax.text(0.02, 0.95, '\n'.join(stats), transform=ax.transAxes,
            fontsize=8, va='top', bbox=dict(facecolor='white', alpha=0.7))
    fname = f"{os.path.splitext(os.path.basename(summary['file']))[0]}_batches.png"
    plt.tight_layout()
    fig.savefig(fname)
    plt.close(fig)
    print(f"Saved plot: {fname}")


def main():
    workers = min(len(file_paths), os.cpu_count() or 1)
    start_all = time.perf_counter()
    print(f"Processing {len(file_paths)} files with {workers} workers...")

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exe:
        results = list(exe.map(process_file, file_paths))

    for summary in results:
        plot_batches(summary)
        print(f"\nFile: {summary['file']}")
        print(f"  Events: {summary['events']}, π⁺={summary['total_pos']}, π⁻={summary['total_neg']}")
        print(f"  Avg±unc: π⁺={summary['avg_pos']:.3f}±{summary['unc_pos']:.3f}, π⁻={summary['avg_neg']:.3f}±{summary['unc_neg']:.3f}")
        print(f"  Δ={summary['diff']}, σ_tot={summary['combined_unc']:.3f}, Signif={summary['significance']:.2f}σ")
        print(f"  Time: {summary['time_s']:.3f}s")

    print(f"Total time: {time.perf_counter() - start_all:.3f}s")

if __name__ == '__main__':
    main()