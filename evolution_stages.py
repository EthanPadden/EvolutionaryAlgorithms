import random

import numpy as np
import settings as g
import tools
from Population import Population
from Solution import Solution
import fitness_functions as f


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
    fitness_function = f.fitness_funtions[g.fitness_fn_num-1]
    for solution in population.get_solutions():
        solution.calc_fitness(fitness_function)

def select_by_sorting(current_gen, next_gen=None):
    # Sort the population by fitness
    current_gen.sort()

    print('SELECTION - SORTED FITNESSES:')
    print(current_gen.to_string())

    output = f'SELECTION - {g.num_selected_solutions} SELECTED:\t\t'
    if(next_gen == None):
        next_gen = Population(current_gen.get_gen_num() + 1)
    for i in range(0, g.num_selected_solutions):
        solution = current_gen.get_solutions()[i]
        next_gen.add_solution(solution)
        output += f"\t{solution.get_fitness()}"

    print(output)
    slots_left = g.population_size - g.num_selected_solutions
    print(f'SELECTION - slots left = {slots_left}')
    return next_gen

def select_by_examining_dominance_relationships(current_gen, next_gen=None):
    '''

    :param current_gen:
    :param next_gen:
    :return:
    '''

    '''
    So we can think of the population as a scatter plot where the x-axis is total_range and the y-axis is total_cost
    Each point is a solution in the population
    Solution A dominates solution B if the total_range is higher and the total_cost is lower in A
    In this case, we can get rid of solution B
    '''
    pass

def variation(current_gen, next_gen):
    current_gen.sort()

    # CROSSOVER
    if g.crossover == True:
        # we need to loop until the next generation is full

        output = 'VARIATION - SORTED FITNESSES:'
        for solution in current_gen.get_solutions():
            output += f"\t{solution.get_fitness()}"
        print(output)

        output = f'VARIATION - {g.num_selected_solutions} NEXT_GEN:\t\t'
        if (next_gen == None):
            next_gen = []
        for i in range(0, g.num_selected_solutions):
            # TODO: change to get_solution(index)?
            solution = current_gen.get_solutions()[i]
            output += f"\t{solution.get_fitness()}"

        print(output)
        slots_left = g.population_size - g.num_selected_solutions
        print(f'VARIATION - slots left = {slots_left}')

        # TODO: get_size() method for population
        while(len(next_gen.get_solutions()) < g.population_size):
            # choose the top 2 in the population - and pop them off so we dont consider them anymore
            parent_a = current_gen.get_solutions().pop(0)
            parent_b = current_gen.get_solutions().pop(0)
            offspring_c, offspring_d = tools.crossover(parent_a, parent_b)
            output = f"CROSSOVER:\t{parent_a.get_config()} + {parent_b.get_config()} = {offspring_c.get_config()} + {offspring_d.get_config()}"
            output += f"\n\t\t\t{str(parent_a.get_fitness())} + {str(parent_b.get_fitness())} = {str(offspring_c.get_fitness())} + {str(offspring_d.get_fitness())}"
            print(output)
            fitness_function = f.fitness_funtions[g.fitness_fn_num-1]
            offspring_c.calc_fitness(fitness_function)
            offspring_d.calc_fitness(fitness_function)
            next_gen.add_solution(offspring_c)
            if len(next_gen.get_solutions()) < g.population_size:
                next_gen.add_solution(offspring_d)
    else:
        # Just fill up the rest of the slots with the sorted population
        next_gen.clear_solutions()
        for solution in current_gen.get_solutions():
            next_gen.add_solution(solution)
    # mutation
    if g.mutation == True:
        next_gen.mutate()
