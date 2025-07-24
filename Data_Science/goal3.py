import math
import time

# Configuration
batch_size = 1000          # Number of events per batch for memory-efficient processing
sigma_threshold = 3.0      # Significance threshold (σ units)
file_paths = [
    '_Data/output-Set0.txt',
    '_Data/output-Set1.txt',
    # Add additional file paths here
]


def calculate_average_and_uncertainty(total_count: float, n_events: int) -> tuple[float, float]:
    """
    Compute average count per event and its Poisson uncertainty on the mean.
    Uncertainty on the mean = sqrt(total_count) / n_events
    """
    if n_events <= 0:
        return float('nan'), float('nan')
    average = total_count / n_events
    uncertainty = math.sqrt(total_count) / n_events if total_count >= 0 else float('nan')
    return average, uncertainty


def check_type(pdg_code: int) -> int:
    """
    Classify particle by PDG code:
    +1 for π⁺ (PDG 211), -1 for π⁻ (PDG -211), 0 otherwise.
    """
    if pdg_code == 211:
        return 1
    elif pdg_code == -211:
        return -1
    else:
        return 0


def process_file(path: str) -> dict:
    """
    Process one data file with event and particle listings.
    Aggregates total positive and negative pion counts in batches.
    Returns a summary dict with counts and statistics.
    """
    total_pos = 0
    total_neg = 0
    event_count = 0
    batch_pos = 0
    batch_neg = 0
    start_time = time.perf_counter()

    with open(path, 'r') as f:
        while True:
            header = f.readline()
            if not header:
                break  # EOF
            parts = header.split()
            if len(parts) != 2:
                continue  # skip malformed lines

            event_count += 1
            _, n_particles = map(int, parts)

            # Count pions in this event
            event_pos = 0
            event_neg = 0
            for _ in range(n_particles):
                *_, pdg_str = f.readline().split()
                typ = check_type(int(pdg_str))
                if typ == 1:
                    event_pos += 1
                elif typ == -1:
                    event_neg += 1

            # Accumulate totals
            total_pos += event_pos
            total_neg += event_neg
            batch_pos += event_pos
            batch_neg += event_neg

            # Reset batch counters periodically to limit memory usage
            if event_count % batch_size == 0:
                batch_pos = 0
                batch_neg = 0

    elapsed = time.perf_counter() - start_time

    # Compute averages and uncertainties
    avg_pos, unc_pos = calculate_average_and_uncertainty(total_pos, event_count)
    avg_neg, unc_neg = calculate_average_and_uncertainty(total_neg, event_count)

    diff = abs(total_pos - total_neg)
    combined_unc = math.hypot(unc_pos, unc_neg)
    significance = diff / combined_unc if combined_unc > 0 else float('inf')

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
        'significance': significance,
        'significant': significance > sigma_threshold,
        'time_s': elapsed
    }


def main():
    overall_start = time.perf_counter()
    print(f"Processing {len(file_paths)} files with batch size = {batch_size} events...")
    for path in file_paths:
        summary = process_file(path)
        print(f"\nFile: {summary['file']}")
        print(f"  Events processed: {summary['events']}")
        print(f"  Total π⁺ = {summary['total_pos']}, Total π⁻ = {summary['total_neg']}")
        print(f"  Average per event: π⁺ = {summary['avg_pos']:.3f} ± {summary['unc_pos']:.3f}, "
              f"π⁻ = {summary['avg_neg']:.3f} ± {summary['unc_neg']:.3f}")
        print(f"  Difference = {summary['diff']}, Combined uncertainty = {summary['combined_unc']:.3f}")
        print(f"  Significance = {summary['significance']:.2f}σ "
              f"({'Significant' if summary['significant'] else 'Not significant'} at {sigma_threshold}σ)")
        print(f"  Processing time: {summary['time_s']:.3f} s")

    total_elapsed = time.perf_counter() - overall_start
    print(f"\nTotal execution time: {total_elapsed:.3f} s")


if __name__ == '__main__':
    main()
