import ast

###
# Loads a data set of random values from the disk
# The "randoms_db.txt" contains one random per line, each containing the random value followed by the zero-based iteration
# where it was generated in the sequence. The method returns two values:
# - the map associating each random value to the list of zero-based iterations where it was generated
# - the total count of iterations
def load_randoms(randoms_file):
    randoms_map = {}
    count = 0
    with open(randoms_file, "r") as data_file:
        for line in data_file.readlines():
            line_parts = line.split(" ", 1)
            random_value = int(line_parts[0])
            random_indexes = ast.literal_eval(line_parts[1])
            randoms_map[random_value] = random_indexes
            count += len(random_indexes)
    return randoms_map, count

if __name__ == "__main__":
    randoms_map, count = load_randoms("IntroToPy/randoms_db.txt")
    print(f"Loaded {len(randoms_map.keys())} unique random generated in a sequence of {count} iterations")
