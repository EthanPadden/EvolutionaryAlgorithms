from math import ceil
import random
import numpy as np
import pandas as pd
from plotly import express as px

def print_population(population):
   for solution in population:
       bitstring = ''.join(map(str, solution['config']))
       fitness = solution['fitness']
       print(f'{bitstring}\t{fitness}')


def fitness(config):
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
    for i in range(0, len(config)):
        if config[i] == 1:
            tower_placements.append(possible_tower_placements[i])
        elif config[i] != 0 and config[i] != 1:
            raise ValueError

    # Sum the variables in this solution
    sum_range = 0
    sum_cost = 0
    for tower_placement in tower_placements:
        sum_range += tower_placement['range']
        sum_cost += tower_placement['cost']

    return (100*sum_range) - sum_cost

def calculate_avg_fitness():
    sum_fitnesses = 0
    for solution in current_generation:
        sum_fitnesses += solution['fitness']

    return sum_fitnesses/len(current_generation)

def crossover(parent_a, parent_b):
    config_a = parent_a['config']
    config_b = parent_b['config']
    crossover_point = ceil(len(config_a)/2)

    config_c = np.concatenate((config_a[:crossover_point], config_b[crossover_point:]))
    config_d = np.concatenate((config_b[:crossover_point], config_a[crossover_point:]))

    offspring_c = {'config': config_c, 'fitness': 0}
    offspring_d = {'config': config_d, 'fitness': 0}

    return offspring_c, offspring_d

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
    # TODO: each solution will have their fitness associated with them and stored
    # solution: { bitstring : fitness }
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

    # Termination criteria variables
    max_generations = 20
    terminate = False
    generation_number = 0
    percentage_performance_stagnation = 5
    previous_avg_fitness = 0

    # Selection variables
    num_selected_solutions = 6

    # INITIALISATION    ===================================
    current_generation = []
    for i in range(0, population_size):
        # create a random bitstring of length T
        bitstring = np.random.randint(0, 2, size=8, dtype=np.uint8)
        # Initially set the fitness value to 0 until we evaluate
        solution = {
            'config': bitstring,
            'fitness': 0
        }
        current_generation.append(solution)

    print_population(current_generation)

    # GENERATIONAL LOOP
    while(terminate == False):
        # EVALUATION        ===================================
        for solution in current_generation:
            config = solution['config']
            solution['fitness'] = fitness(config)

        print_population(current_generation)

        # TERMINATION       ===================================
        # In this problem, we don't have an ideal fitness if we can improve the cost-range tradeoff
        # So no fitness condition

        # Max generations reached?
        if generation_number >= max_generations:
            terminate = True
            break

        # Performance stagnation?
        # Instead of a threshold value, we can take this as a percentage
        # ie if we don't see an increase of at least 5% for the average fitness, stop
        current_avg_fitness = calculate_avg_fitness()
        diff_avg_fitness = current_avg_fitness - previous_avg_fitness
        if(generation_number > 0):
            if ((diff_avg_fitness/previous_avg_fitness) * 100) < 5:
                terminate = True
                break

        # SELECTION       ===================================
        # Sort the population by fitness
        sorted_population = sorted(current_generation, key=lambda x: x['fitness'], reverse=True)
        next_generation = []
        for i in range(0, num_selected_solutions):
            next_generation.append(sorted_population[i])

        # VARIATION       ===================================
        # crossover
        # we need to loop until the next generation is full
        while(len(next_generation) < len(current_generation)):
            # choose the top 2 in the population - and pop them off so we dont consider them anymore
            parent_a = sorted_population.pop(0)
            parent_b = sorted_population.pop(0)
            offspring_c, offspring_d = crossover(parent_a, parent_b)
            next_generation.append(offspring_c)
            if len(next_generation) < len(current_generation):
                next_generation.append(offspring_d)

        # mutation
        # choose a random number of solutions
        num_solutions_to_mutate = random.randint(1, len(next_generation))
        for i in range(1, num_solutions_to_mutate):
            # choose a random solution

            soln_index_to_mutate = random.randint(0, (len(next_generation)-1))
            soln_to_mutate = next_generation[soln_index_to_mutate]

            # choose a random number of bits to flip
            num_bits_to_flip = random.randint(0, (len(possible_tower_placements)-1))

            for i in range(0, num_bits_to_flip):
                # choose a random bit and flip it
                bit_index_to_flip = random.randint(0, (len(possible_tower_placements)-1))
                config = soln_to_mutate['config']
                if config[bit_index_to_flip] == 0:
                    config[bit_index_to_flip] = 1
                elif config[bit_index_to_flip] == 1:
                    config[bit_index_to_flip] = 0
                else:
                    raise ValueError()

        previous_avg_fitness = current_avg_fitness
        generation_number += 1









