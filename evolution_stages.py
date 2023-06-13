import random

import numpy as np
import settings as g
import tools
from Population import Population
from Solution import Solution


def initialise():
    population = Population(0)

    for i in range(0, g.population_size):
        # create a random bitstring of length T
        bitstring = np.random.randint(0, 2, size=8, dtype=np.uint8)
        # Initially set the fitness value to 0 until we evaluate
        solution = Solution(bitstring)
        population.add_solution(solution)

    return population

def evaluate(population):
    for solution in population:
        config = solution['config']
        solution['fitness'] = tools.fitness(config)

def select(current_gen, next_gen=None):
    # Sort the population by fitness
    sorted_population = sorted(current_gen, key=lambda x: x['fitness'], reverse=True)

    output = 'SELECTION - SORTED FITNESSES:'
    for solution in sorted_population:
        output += f"\t{solution['fitness']}"
    print(output)

    output = f'SELECTION - {g.num_selected_solutions} SELECTED:\t\t'
    if(next_gen == None):
        next_gen = []
    for i in range(0, g.num_selected_solutions):
        solution = sorted_population[i]
        next_gen.append(solution)
        output += f"\t{solution['fitness']}"

    print(output)
    slots_left = g.population_size - g.num_selected_solutions
    print(f'SELECTION - slots left = {slots_left}')
    return next_gen

def variation(current_gen, next_gen):
    # CROSSOVER
    # we need to loop until the next generation is full
    sorted_population = sorted(current_gen, key=lambda x: x['fitness'], reverse=True)

    output = 'VARIATION - SORTED FITNESSES:'
    for solution in sorted_population:
        output += f"\t{solution['fitness']}"
    print(output)

    output = f'VARIATION - {g.num_selected_solutions} NEXT_GEN:\t\t'
    if (next_gen == None):
        next_gen = []
    for i in range(0, g.num_selected_solutions):
        solution = sorted_population[i]
        output += f"\t{solution['fitness']}"

    print(output)
    slots_left = g.population_size - g.num_selected_solutions
    print(f'VARIATION - slots left = {slots_left}')

    while(len(next_gen) < len(current_gen)):
        # choose the top 2 in the population - and pop them off so we dont consider them anymore
        parent_a = sorted_population.pop(0)
        parent_b = sorted_population.pop(0)
        offspring_c, offspring_d = tools.crossover(parent_a, parent_b)
        output = f"CROSSOVER:\t{parent_a['config']} + {parent_b['config']} = {offspring_c['config']} + {offspring_d['config']}"
        output += f"\n\t\t\t{str(parent_a['fitness'])} + {str(parent_b['fitness'])} = {str(offspring_c['fitness'])} + {str(offspring_d['fitness'])}"
        print(output)
        next_gen.append(offspring_c)
        if len(next_gen) < len(current_gen):
            next_gen.append(offspring_d)

    # mutation
    # choose a random number of solutions
    num_solutions_to_mutate = random.randint(1, len(next_gen))
    for i in range(1, num_solutions_to_mutate):
        # choose a random solution

        soln_index_to_mutate = random.randint(0, (len(next_gen) - 1))
        soln_to_mutate = next_gen[soln_index_to_mutate]

        # choose a random number of bits to flip
        num_bits_to_flip = random.randint(0, (len(g.possible_tower_placements) - 1))

        for i in range(0, num_bits_to_flip):
            # choose a random bit and flip it
            bit_index_to_flip = random.randint(0, (len(g.possible_tower_placements) - 1))
            config = soln_to_mutate['config']
            if config[bit_index_to_flip] == 0:
                config[bit_index_to_flip] = 1
            elif config[bit_index_to_flip] == 1:
                config[bit_index_to_flip] = 0
            else:
                raise ValueError