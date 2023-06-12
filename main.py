import numpy as np
import pandas as pd
from plotly import express as px

def print_population(population):
    for solution in population:
        bitstring = ''.join(map(str, solution))
        print(bitstring)

if __name__ == '__main__':
    '''Single-objective problem:
    Problem: Optimizing the Placement of Cell Towers for Maximum Coverage
    * Imagine you are a telecommunication company tasked with optimizing the placement of cell towers in a given region to provide maximum coverage and minimize signal interference.
    The objective is to determine the optimal locations for the cell towers to ensure the widest possible coverage while minimizing the number of towers needed.
    * In this problem, you are provided with a map of the region and need to decide where to place the cell towers.
    Each potential tower location has associated coverage radius and cost.
    The coverage radius determines the area in which the tower can provide reliable signal strength.
    The cost represents the expense of installing and maintaining the tower.
    * The goal is to find the optimal set of tower locations that maximizes the coverage area while minimizing the total cost of installation and maintenance.
    '''
    # Lets say we have a fixed number T of possible tower locations (easier to zero index)
    # [t0, t1, ..., tT]
    # Each solution will be a configuration of tower placements out of the possible T tower placements
    # Each tower placement has an associated radius and cost
    # We want to maximise radius while minimising cost
    # This does not take signal interference or overlap into account TODO: ?

    # Solution representation:
    # configuration consists of 3 towers
    # since each tower location is at a set index, we can use a bitstring of length T
    # e.g. if T = 8 config [t2, t5, t6] can be represented as 00100110
    # population consists of N possible tower configurations

    # GLOBAL VARIABLES (CAN BE ADJUSTED)
    T = 8
    population_size = 10

    # INITIALISATION
    population = []
    for i in range(0, population_size):
        # create a random bitstring of length T
        solution = np.random.randint(0, 2, size=8, dtype=np.uint8)
        population.append(solution)

    print_population(population)






