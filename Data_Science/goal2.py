import math
import matplotlib.pyplot as plt
import numpy as np

sigma_threshold = 0.05
batch_size = 10000


def check_type(pdg_code: int) -> int:
    if pdg_code == 211:
        return 1
    elif pdg_code == -211:
        return -1
    return 0


def poisson_uncertainty(count: float) -> float:
    return math.sqrt(count)


def difference(no1: float, no2: float) -> float:
    return abs(no1 - no2)


def combined_uncertainty(sigma1: float, sigma2: float) -> float:
    return math.hypot(sigma1, sigma2)


def significance(diff: float, comb_unc: float) -> float:
    return diff / comb_unc if comb_unc > 0 else float('inf')


def process_events(input_path: str):
    total_pos = total_neg = 0
    event_count = 0

    pos_batches = []
    neg_batches = []
    batch_pos = batch_neg = 0

    try:
        with open(input_path, 'r') as f:
            while True:
                header = f.readline()
                if not header:
                    break
                parts = header.split()
                if len(parts) != 2:
                    continue
                _, count = map(int, parts)
                event_count += 1
                for _ in range(count):
                    *_, pdg_str = f.readline().split()
                    typ = check_type(int(pdg_str))
                    if typ == 1:
                        total_pos += 1
                        batch_pos += 1
                    elif typ == -1:
                        total_neg += 1
                        batch_neg += 1
                if event_count % batch_size == 0:
                    pos_batches.append(batch_pos)
                    neg_batches.append(batch_neg)
                    batch_pos = batch_neg = 0
    except FileNotFoundError:
        print(f"Error: '{input_path}' not found.")
        return
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
        return

    if batch_pos or batch_neg:
        pos_batches.append(batch_pos)
        neg_batches.append(batch_neg)

    if event_count == 0:
        print("No events processed.")
        return

    avg_pos = total_pos / event_count
    avg_neg = total_neg / event_count
    sigma_pos = poisson_uncertainty(total_pos)
    sigma_neg = poisson_uncertainty(total_neg)
    diff = difference(total_pos, total_neg)
    sigma_comb = combined_uncertainty(sigma_pos, sigma_neg)
    sig = significance(diff, sigma_comb)

    # Print summary
    summary_lines = [
        f"Processed {event_count} events.",
        f"Total: {total_pos} π⁺, {total_neg} π⁻",
        f"Average per event: {avg_pos:.3f} π⁺, {avg_neg:.3f} π⁻",
        f"Poisson σ: {sigma_pos:.2f} (π⁺), {sigma_neg:.2f} (π⁻)",
        f"Difference: {diff}",
        f"Combined σ: {sigma_comb:.2f}",
        f"Significance: {sig:.2f}σ ({'Significant' if sig>=sigma_threshold else 'Not significant'})"
    ]
    for line in summary_lines:
        print(line)

    # Plotting
    batches = len(pos_batches)
    x = np.arange(1, batches + 1) * batch_size
    plt.figure(figsize=(8, 5))
    plt.plot(x, pos_batches, marker='o', label='π⁺')
    plt.plot(x, neg_batches, marker='s', label='π⁻')
    plt.grid(True)
    plt.xlabel('Events processed')
    plt.ylabel(f'Counts per {batch_size} events')
    plt.title('Batch-wise Pion Counts')
    plt.legend()

    # Annotate summary on plot
    text_x = 0.02  # fraction of axis width
    text_y = 0.95
    plt.gca().text(
        text_x, text_y,
        "\n".join(summary_lines),
        transform=plt.gca().transAxes,
        fontsize=8,
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7)
    )

    plt.tight_layout()
    output_file = 'pion_counts.png'
    plt.savefig(output_file, dpi=150)
    print(f"Plot saved as '{output_file}'")


if __name__ == '__main__':
    process_events('_Data/output-Set1.txt')