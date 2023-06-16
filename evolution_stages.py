import copy
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
    current_gen.sort_by_fitness()

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
    
    So should we go through every combination of 2 solutions - seems inefficient
    Better:
    sort the solutions by total_range - as if we are looking right to left on the plot
    Take the first solution A (the farthest right) and work through the list for every other solution Bi - FROM WORST TO BEST!!!
    If the total_cost of A < total_cost of Bi then get rid of Bi because A dominates Bi
    Now this will leave a list of solutions of length s E [1, len(current_gen)]
    Should we now choose the second of the list (if s > 2) to see if it dominates the rest?
    Maybe we can try doing this until the list reaches a certain length defined in the settings
    - do the results differ much if we first sort by total_cost (ascending)
    '''
    # Sort solutions by range
    # TODO: setting for cost instead
    current_gen.sort_by_range()

    # TODO: make more concise - using deepcopy of an object?
    # TODO: make consistent with other selction method
    next_gen_solns = copy.deepcopy(current_gen.get_solutions())
    if (next_gen == None):
        next_gen = Population(current_gen.get_gen_num() + 1)
    for solution in next_gen_solns:
        next_gen.add_solution(solution)

    # This is the index of the solution we are considering (comparing to all others)
    compare_index = 0
    while (len(next_gen.get_solutions()) > g.num_selected_solutions) and compare_index < len(current_gen.get_solutions()):
        # Solution we are considering out of the current generation
        compare_soln = current_gen.get_solutions()[compare_index]

        # For every other solution - worst to best
        for other_soln_index in range((len(next_gen.get_solutions())-1), compare_index, -1):
            if len(next_gen.get_solutions()) == g.num_selected_solutions:
                break
            elif len(next_gen.get_solutions()) < g.num_selected_solutions:
                raise ValueError
            # Solution to compare to out of the next generation
            other_soln = next_gen.get_solutions()[other_soln_index]
            # we can use the dominates method regardless of which member the solutions were sorted by
            if compare_soln.dominates(other_soln):
                # get rid of the other solution in the next generation
                next_gen.get_solutions().pop(other_soln_index)

        # Now we move onto the next solution
        compare_index += 1

    # At this point, the compare index could reach the end of the population before next_gen has reached the target size
    # In this case, we just remove the worst solutions until the next_gen is of the target size
    while (len(next_gen.get_solutions()) > g.num_selected_solutions):
        next_gen.get_solutions().pop()

    return next_gen


def variation(current_gen, next_gen):
    current_gen.sort_by_fitness()

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
