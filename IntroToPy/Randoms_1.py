import random

# Read input parameters from the console
count = 100 # int(input("Number of values?> "))
min_value = 15 # int(input("Minimum value?> "))
max_value = 65 # int(input("Maximum value?> "))
print(f"Generating {count} randoms in the range [{min_value}, {max_value}]")

# Generate count values in the range [min_value, max_value] and store them in a the values map
# randoms_map - associates each random value to the zero-based index/iteration where it was generated
# <key=random_value, value=[index1, index2, index3, ...]> 
randoms_map = {}
for i in range(0, count):
    r = random.randint(min_value, max_value)
    #r = int(min_value + i) if i < 9 * count/10 else min_value + 1000 + i
    if r not in randoms_map:
        randoms_map[r] = []
    randoms_map[r].append(i)

# Write a text file "randoms_db.txt" with each random on a line, its value followed by the indexes where it occurred
with open("IntroToPy/randoms_db.txt", "w") as data_file:
    for r in randoms_map.keys():
        data_file.write(f"{r} {randoms_map[r]}\n")

