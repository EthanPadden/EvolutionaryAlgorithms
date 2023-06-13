from math import ceil
import random
import numpy as np
import tools
import settings as g
import evolution_stages as evo

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

    # INITIALISATION    ===================================
    current_generation = evo.initialise()
    tools.print_population(current_generation, -1)

    # GENERATIONAL LOOP
    generation_number = 0
    # TODO: remove this variable - not needed? just use break?
    terminate = False
    previous_avg_fitness = 0
    while(terminate == False):
        # EVALUATION        ===================================
        evo.evaluate(current_generation)

        # TERMINATION       ===================================
        # In this problem, we don't have an ideal fitness if we can improve the cost-range tradeoff
        # So no fitness condition

        # Max generations reached?
        if generation_number >= g.max_generations:
            terminate = True
            break

        # Performance stagnation?
        # Instead of a threshold value, we can take this as a percentage
        # ie if we don't see an increase of at least 5% for the average fitness, stop
        current_avg_fitness = tools.calculate_avg_fitness(current_generation)
        diff_avg_fitness = current_avg_fitness - previous_avg_fitness
        if(generation_number > 0):
            if ((diff_avg_fitness/previous_avg_fitness) * 100) < 5:
                terminate = True
                break

        # SELECTION       ===================================
        # Sort the population by fitness
        sorted_population = sorted(current_generation, key=lambda x: x['fitness'], reverse=True)
        next_generation = []
        for i in range(0, g.num_selected_solutions):
            next_generation.append(sorted_population[i])

        # VARIATION       ===================================
        # crossover
        # we need to loop until the next generation is full
        while(len(next_generation) < len(current_generation)):
            # choose the top 2 in the population - and pop them off so we dont consider them anymore
            parent_a = sorted_population.pop(0)
            parent_b = sorted_population.pop(0)
            offspring_c, offspring_d = tools.crossover(parent_a, parent_b)
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
            num_bits_to_flip = random.randint(0, (len(g.possible_tower_placements)-1))

            for i in range(0, num_bits_to_flip):
                # choose a random bit and flip it
                bit_index_to_flip = random.randint(0, (len(g.possible_tower_placements)-1))
                config = soln_to_mutate['config']
                if config[bit_index_to_flip] == 0:
                    config[bit_index_to_flip] = 1
                elif config[bit_index_to_flip] == 1:
                    config[bit_index_to_flip] = 0
                else:
                    raise ValueError

        previous_avg_fitness = current_avg_fitness
        generation_number += 1









