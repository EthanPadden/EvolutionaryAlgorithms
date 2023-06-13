import random

import numpy as np
import settings as g
import tools


def initialise():
    population = []
    for i in range(0, g.population_size):
        # create a random bitstring of length T
        bitstring = np.random.randint(0, 2, size=8, dtype=np.uint8)
        # Initially set the fitness value to 0 until we evaluate
        solution = {
            'config': bitstring,
            'fitness': 0
        }
        population.append(solution)

    return population

def evaluate(population):
    for solution in population:
        config = solution['config']
        solution['fitness'] = tools.fitness(config)

def select(current_gen, next_gen=None):
    # Sort the population by fitness
    sorted_population = sorted(current_gen, key=lambda x: x['fitness'], reverse=True)
    if(next_gen == None):
        next_gen = []
    for i in range(0, g.num_selected_solutions):
        next_gen.append(sorted_population[i])

    return next_gen

def variation(current_gen, next_gen):
    # crossover
    # we need to loop until the next generation is full
    sorted_population = sorted(current_gen, key=lambda x: x['fitness'], reverse=True)
    while(len(next_gen) < len(current_gen)):
                # choose the top 2 in the population - and pop them off so we dont consider them anymore
                parent_a = sorted_population.pop(0)
                parent_b = sorted_population.pop(0)
                offspring_c, offspring_d = tools.crossover(parent_a, parent_b)
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