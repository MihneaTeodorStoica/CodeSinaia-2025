import math


def calculate_p(px: float, py: float, pz: float) -> float:
    return math.sqrt(px**2 + py**2 + pz**2)


def calculate_pT(px: float, py: float) -> float:
    return math.sqrt(px**2 + py**2)


def calculate_pseudorapidity(pz: float, p: float) -> float:
    argument = (p + pz) / (p - pz)
    return 0.5 * math.log(argument) if argument > 0 else float('nan')


def calculate_azimuthal_angle(px: float, py: float) -> float:
    return math.atan2(py, px)

def check_type(pdg_code: int) -> str:
    pdg_map = {
        211: 'Pi +', -211: 'Pi -',
    }
    return pdg_map.get(pdg_code, f'unknown (PDG {pdg_code})')


def process_event(event_id: int, num_particles: int, particle_lines: list[str]) -> None:
    print(f"Event {event_id}: {num_particles} entries:")

    for idx, line in enumerate(particle_lines, start=1):
        px, py, pz, pdg = line
        px, py, pz = float(px), float(py), float(pz)
        pdg = int(pdg)

        p = calculate_p(px, py, pz)
        pT = calculate_pT(px, py)
        eta = calculate_pseudorapidity(pz, p)
        phi = calculate_azimuthal_angle(px, py)
        name = check_type(pdg)

        print(f"  [{idx}] {name}: px = {px}, py = {py}, pz = {pz}")
        print(f"    p = {p:.8f}, pT = {pT:.8f}, eta = {eta:.8f}, phi = {phi:.8f}")
    print()


def main(input_path: str) -> None:
    with open(input_path, 'r') as f:
        while True:
            header = f.readline()
            if not header:
                break  # EOF reached

            parts = header.split()
            if len(parts) != 2:
                continue  # Skip malformed or blank lines

            event_id, count = map(int, parts)
            lines = [f.readline().split() for _ in range(count)]

            process_event(event_id, count, lines)


if __name__ == "__main__":
    main("_Data/output-Set0.txt")
