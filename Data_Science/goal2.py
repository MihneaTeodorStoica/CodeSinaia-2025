import math
import matplotlib.pyplot as plt
import numpy as np

threshold = 0.05

# Returns 1 for positive pion (211), -1 for negative pion (-211), 0 otherwise
def check_type(pdg_code):
    pass  # TODO: Implement this function

# Returns the Poisson uncertainty for a given average
def poisson_distribution(average):
    pass  # TODO: Implement this function

# Returns the absolute difference between two numbers
def difference(no_1, no_2):
    pass  # TODO: Implement this function

# Returns the combined uncertainty for two numbers
def combined_uncertainty(no_1, no_2):
    pass  # TODO: Implement this function

# Returns the significance of the difference
def significance(no_1, no_2, comb_uncertainty):
    pass  # TODO: Implement this function

# TODO: Open the input file, read the first line to get event_id and num_particles,
#       then read the rest of the lines into lines_list as lists of strings.
#       Handle FileNotFoundError and IOError with appropriate messages--> handle file errors.

# TODO: Loop through each particle in lines_list, convert values to float,
#       use check_type to count positive and negative pions per event.

# TODO: You may use batching (e.g., sum per 1000 events) or sampling (store per-event counts).
#       Batching is recommended for large files to reduce memory usage.
#       Sampling (storing per-event counts) is useful if you want to analyze or plot per-event data.

# TODO: After processing, print the total number of positive and negative pions,
#       their averages per event, Poisson uncertainties, the difference, combined uncertainty, and significance.
#       Print whether the significance is above the threshold.

# TODO: Plot a single graph showing the number of positive and negative pions in each batch of 1000 events.
#       X-axis: event number (0, 1000, 2000, ...)
#       Y-axis: number of pions in each batch of 1000 events
#       The plot should have two lines: one for positive pions, one for negative pions.

# Example expected output (printed):
# In 500000 total events, we had 9238697 positive particles and 9225784 negative particles.
# there s an average of  18.477394 particles(positive pions)
# there s an average of  18.451568 anti-particles(negative pions)
# the poisson distribution for the positive pions is 3039.52 ...
# the poisson distribution for the negative(antiparticle) pions is 3037.39 ...
# there are  12913  more particles then antiparticles
# the combined uncertainty of the total amount of particles and antiparticles is  4297.03 ...
# the significance is  3.00 ...
# the significance is very large compared to the threshold

# Example expected plot:
# A line plot with two lines (positive and negative pions per 1000 events), x-axis labeled "Event number", y-axis labeled "Number of pions in 1000 events".