import math
import matplotlib.pyplot as plt
import numpy as np
import time

# Configuration
batch_size = 1000          # events per batch when batching
sample_rate = 1000         # process one event every N events
sigma_threshold = 3.0      # significance threshold (σ units)


def check_type(pdg_code: int) -> int:
    """
    Classify: +1 for π⁺ (PDG 211), -1 for π⁻ (PDG -211), 0 otherwise.
    """
    return 1 if pdg_code == 211 else -1 if pdg_code == -211 else 0


def poisson_uncertainty(count: float) -> float:
    """Poisson σ = √count"""
    return math.sqrt(count)


def difference(a: float, b: float) -> float:
    """Absolute difference"""
    return abs(a - b)


def combined_uncertainty(s1: float, s2: float) -> float:
    """σ_comb = √(s1² + s2²)"""
    return math.hypot(s1, s2)


def significance(diff: float, comb: float) -> float:
    """Z-score significance"""
    return diff / comb if comb > 0 else float('inf')


def process_events_batch(path: str):
    """
    Full pass: tally π⁺/π⁻ per batch of batch_size events.
    Returns summary dict and per-batch counts.
    """
    total_pos = total_neg = 0
    event_idx = 0
    pos_batches, neg_batches = [], []
    batch_pos = batch_neg = 0

    with open(path) as f:
        while True:
            header = f.readline()
            if not header:
                break
            parts = header.split()
            if len(parts) != 2:
                continue
            _, count = map(int, parts)
            event_idx += 1
            for _ in range(count):
                *_, pdg = f.readline().split()
                typ = check_type(int(pdg))
                total_pos += (typ == 1)
                total_neg += (typ == -1)
                batch_pos += (typ == 1)
                batch_neg += (typ == -1)

            if event_idx % batch_size == 0:
                pos_batches.append(batch_pos)
                neg_batches.append(batch_neg)
                batch_pos = batch_neg = 0

    # remainder
    if batch_pos or batch_neg:
        pos_batches.append(batch_pos)
        neg_batches.append(batch_neg)

    avg_pos = total_pos / event_idx
    avg_neg = total_neg / event_idx
    sigma_pos = poisson_uncertainty(total_pos)
    sigma_neg = poisson_uncertainty(total_neg)
    diff = difference(total_pos, total_neg)
    sigma_comb = combined_uncertainty(sigma_pos, sigma_neg)
    z = significance(diff, sigma_comb)

    summary = {
        'mode': 'batch',
        'events': event_idx,
        'total_pos': total_pos,
        'total_neg': total_neg,
        'avg_pos': avg_pos,
        'avg_neg': avg_neg,
        'sigma_pos': sigma_pos,
        'sigma_neg': sigma_neg,
        'diff': diff,
        'sigma_comb': sigma_comb,
        'significance': z,
    }
    return summary, pos_batches, neg_batches


def process_events_subsample(path: str):
    """
    Subsampling pass: process only every sample_rate-th event.
    Returns summary dict and per-sample counts.
    """
    sampled_pos = sampled_neg = 0
    sample_events, pos_samples, neg_samples = [], [], []
    event_idx = 0

    with open(path) as f:
        while True:
            header = f.readline()
            if not header:
                break
            parts = header.split()
            if len(parts) != 2:
                continue
            _, count = map(int, parts)
            event_idx += 1
            if event_idx % sample_rate == 0:
                pos_count = neg_count = 0
                for _ in range(count):
                    *_, pdg = f.readline().split()
                    typ = check_type(int(pdg))
                    pos_count += (typ == 1)
                    neg_count += (typ == -1)
                sampled_pos += pos_count
                sampled_neg += neg_count
                sample_events.append(event_idx)
                pos_samples.append(pos_count)
                neg_samples.append(neg_count)
            else:
                for _ in range(count): f.readline()

    est_total_events = event_idx
    scale = sample_rate
    est_total_pos = sampled_pos * scale
    est_total_neg = sampled_neg * scale

    avg_pos = est_total_pos / est_total_events
    avg_neg = est_total_neg / est_total_events
    sigma_pos = poisson_uncertainty(est_total_pos)
    sigma_neg = poisson_uncertainty(est_total_neg)
    diff = difference(est_total_pos, est_total_neg)
    sigma_comb = combined_uncertainty(sigma_pos, sigma_neg)
    z = significance(diff, sigma_comb)

    summary = {
        'mode': 'sample',
        'events': est_total_events,
        'sampled_events': len(sample_events),
        'total_pos': est_total_pos,
        'total_neg': est_total_neg,
        'avg_pos': avg_pos,
        'avg_neg': avg_neg,
        'sigma_pos': sigma_pos,
        'sigma_neg': sigma_neg,
        'diff': diff,
        'sigma_comb': sigma_comb,
        'significance': z,
    }
    return summary, sample_events, pos_samples, neg_samples


def main(path: str):
    # Run both modes and time them\    
    start = time.perf_counter()
    summary_b, pos_b, neg_b = process_events_batch(path)
    time_b = time.perf_counter() - start

    start = time.perf_counter()
    summary_s, events_s, pos_s, neg_s = process_events_subsample(path)
    time_s = time.perf_counter() - start

    # Prepare annotation text
    batch_lines = [
        f"Batch mode ({time_b:.3f}s)",
        f"Events: {summary_b['events']}",
        f"Total π⁺={summary_b['total_pos']}, π⁻={summary_b['total_neg']}",
        f"Avg/event: {summary_b['avg_pos']:.3f}, {summary_b['avg_neg']:.3f}",
        f"Poisson uncertainty: {summary_b['sigma_pos']:.2f}, {summary_b['sigma_neg']:.2f}",
        f"Δ={summary_b['diff']}",
        f"Z={summary_b['significance']:.2f}σ"
    ]
    sample_lines = [
        f"Sample mode ({time_s:.3f}s)",
        f"Events: {summary_s['events']}, Samples: {summary_s['sampled_events']}",
        f"Est Total π⁺={summary_s['total_pos']}, π⁻={summary_s['total_neg']}",
        f"Avg/event: {summary_s['avg_pos']:.3f}, {summary_s['avg_neg']:.3f}",
        f"Poisson uncertainty: {summary_s['sigma_pos']:.2f}, {summary_s['sigma_neg']:.2f}",
        f"Δ={summary_s['diff']}",
        f"Z={summary_s['significance']:.2f}σ"
    ]

    # Plot all three panels with annotations
    fig, axes = plt.subplots(3, 1, figsize=(10, 18))
    # Batch counts
    x_b = np.arange(1, len(pos_b)+1) * batch_size
    axes[0].plot(x_b, pos_b, label='π⁺ per batch')
    axes[0].plot(x_b, neg_b, label='π⁻ per batch')
    axes[0].legend()
    axes[0].set_ylabel(f'Counts per {batch_size}')
    axes[0].text(0.02, 0.95, '\n'.join(batch_lines), transform=axes[0].transAxes,
                 fontsize=9, va='top', bbox=dict(facecolor='white', alpha=0.7))

    # Sample counts
    axes[1].plot(events_s, pos_s, label='π⁺ per sample')
    axes[1].plot(events_s, neg_s, label='π⁻ per sample')
    axes[1].legend()
    axes[1].set_ylabel(f'Counts per {sample_rate}')
    axes[1].text(0.02, 0.95, '\n'.join(sample_lines), transform=axes[1].transAxes,
                 fontsize=9, va='top', bbox=dict(facecolor='white', alpha=0.7))

    # Time comparison
    modes = ['batch', 'sample']
    times = [time_b, time_s]
    axes[2].bar(modes, times, color=['tab:blue','tab:orange'])
    axes[2].set_ylabel('Time (s)')
    axes[2].set_title('Processing Time')

    plt.xlabel('Mode', labelpad=15)
    plt.tight_layout()
    plt.savefig('combined_analysis.png', dpi=150)
    print("Combined plot saved: combined_analysis.png")

if __name__ == '__main__':
    main('_Data/output-Set1.txt')
