import numpy as np
import pandas as pd
from plotly import express as px

def print_population(population, solution_fitnesses=None):
   for i in range(0, len(population)):
        solution = population[i]
        bitstring = ''.join(map(str, solution))
        if solution_fitnesses != None:
            fitness = solution_fitnesses[i]
            print(f'{bitstring}\t{fitness}')
        else:
            print(bitstring)


def fitness(solution):
    '''What could be a fitness function here?
    Maximise range
    Minimise cost
    Could be sum(range) - sum(cost)
    The issue with this is if we are measuring in km and euro, the cost values far exceeds the ranges
    this leads to negative fitness values
    Also - the fitness value for no tower placements should intuitively be 0, and should be the worst possible outcome
    Any other combination should lead to a fitness value more than 0
    multiply the range by 100 - same as converting km to m
    TODO: introduce some kind of weights - it would depend on how important each variable is
    TODO: also - is there a maximum cost that we cannot exceed?
    TODO: similarly - is there a minimum range below which the solution is not viable?
    '''
    # Get the corresponding tower placements as in the bitstring
    tower_placements = []
    for i in range(0, len(solution)):
        if solution[i] == 1:
            tower_placements.append(possible_tower_placements[i])
        elif solution[i] != 0 and solution[i] != 1:
            raise ValueError

    # Sum the variables in this solution
    sum_range = 0
    sum_cost = 0
    for tower_placement in tower_placements:
        sum_range += tower_placement['range']
        sum_cost += tower_placement['cost']

    return (100*sum_range) - sum_cost


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
    possible_tower_placements = [
        {'range': 319, 'cost': 578},
        {'range': 449, 'cost': 4937},
        {'range': 771, 'cost': 4552},
        {'range': 887, 'cost': 1819},
        {'range': 722, 'cost': 1932},
        {'range': 569, 'cost': 1958},
        {'range': 760, 'cost': 3122},
        {'range': 600, 'cost': 1320}
    ]

    # INITIALISATION
    population = []
    for i in range(0, population_size):
        # create a random bitstring of length T
        solution = np.random.randint(0, 2, size=8, dtype=np.uint8)
        population.append(solution)

    print_population(population)

    # EVALUATION
    solution_fitnesses = []
    for solution in population:
        solution_fitnesses.append(
            fitness(solution)
        )

    print_population(population, solution_fitnesses)








