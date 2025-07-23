import ast

###
# Loads a dataset of mountains from the disk
# The "mountains_db.tsv" contains one mountain per line, each line containing
# several fields separated by TAB: mountain name, elevantion, country where it is located and
# the ISO3 code of that country.
# The method returns two values:
# - the map associating each country to the list of {mountain, elevation} pairs from within
# - the total count of mountains in the database
def load_mountains(mountains_file):
    mountains_map = {}
    count = 0
    with open(mountains_file, "r", encoding="utf-8-sig") as data_file:
        for line in data_file.readlines():
            line_parts = line.split("\t")
            mountain_name = line_parts[0]
            mountain_elevation = ast.literal_eval(line_parts[1]) if line_parts[1] != "NULL" else None
            country_name = line_parts[2]
            country_iso = line_parts[3]
            if not country_name in mountains_map:
                mountains_map[country_name] = []
            mountains_map[country_name].append({"name":mountain_name, "elevation":mountain_elevation})
            count += 1
    return mountains_map, count

###
# Loads a dataset of mountains from the disk.
# The method returns two values:
# - a map associating each country ISO to the list of {mountain, elevation} pairs from within
# - a map associating each country ISO to the country's full name. 
def load_mountains2(mountains_file):
    mountains_map = {}
    countries_map = {}
    with open(mountains_file, "r", encoding="utf-8-sig") as data_file:
        for line in data_file.readlines():
            line_parts = line.strip().split("\t")
            mountain_name = line_parts[0]
            mountain_elevation = ast.literal_eval(line_parts[1]) if line_parts[1] != "NULL" else None
            country_name = line_parts[2]
            country_iso = line_parts[3]
            if not country_iso in mountains_map:
                mountains_map[country_iso] = []
                countries_map[country_iso] = country_name
            mountains_map[country_iso].append({"name":mountain_name, "elevation":mountain_elevation})
    return mountains_map, countries_map

###
# Loads a dataset of mountains and a dataset of countries into two sets in memory. The sets contain
# objects, one for each row in the file, with the fields corresponding to the columns in the files.
# The method returns the two sets.
# - a set listing all mountains [{name, elevation, country, country_iso}]
# - a set listing all countries [[country_iso, continent]]
def load_mountains3(mountains_file, countries_file):
    mountains_set = []
    with open(mountains_file, "r", encoding="utf-8-sig") as data_file:
        for line in data_file.readlines():
            line_parts = line.strip().split("\t")
            mountains_set.append({
                "name": line_parts[0],
                "elevation": ast.literal_eval(line_parts[1]) if line_parts[1] != "NULL" else None,
                "country" : line_parts[2],
                "country_iso" : line_parts[3]
            })
    countries_set = []
    with open(countries_file, "r", encoding="utf-8-sig") as data_file:
        for line in data_file.readlines():
            line_parts = line.strip().split("\t")
            countries_set.append({
                "country_iso": line_parts[0],
                "continent" : line_parts[1]
            })
    return mountains_set, countries_set


if __name__ == "__main__":
    mountains_map, count = load_mountains("IntroToPy/mountains_db.tsv")
    print(f"Loaded {count} mountains from {len(mountains_map.keys())} countries.")
