import numpy as np
import math
import settings as g
import tkinter as tk
from tkinter import ttk

def print_population(population, generation_number):
    window = tk.Tk()

    # Create a label widget
    label = tk.Label(window, text=f'Generation = {generation_number}')

    # Add the label to the window
    label.pack()

    # Create a Treeview widget
    tree = ttk.Treeview(window, columns=('bitstring', 'fitness', 'Erange', 'Ecost'), show='headings')

    # Set column headers
    tree.heading('bitstring', text='bitstring')
    tree.heading('fitness', text='fitness')
    tree.heading('Erange', text='Erange')
    tree.heading('Ecost', text='Ecost')

    for solution in population:
        config = solution['config']

        bitstring = ''.join(map(str, config))
        fitness = solution['fitness']
        tower_placements = []

        for i in range(0, len(config)):
            if config[i] == 1:
                tower_placements.append(g.possible_tower_placements[i])
            elif config[i] != 0:
                raise ValueError

        total_range = 0
        total_cost = 0
        for tower_placement in tower_placements:
            total_range += tower_placement['range']
            total_cost += tower_placement['cost']

        tree.insert('', 'end', values=(f'{bitstring}', f'{fitness}', f'{total_range}', f'{total_cost}'))

    # Add the Treeview to the window
    tree.pack()

    window.mainloop()

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
            tower_placements.append(g.possible_tower_placements[i])
        elif config[i] != 0 and config[i] != 1:
            raise ValueError

    # Sum the variables in this solution
    sum_range = 0
    sum_cost = 0
    for tower_placement in tower_placements:
        sum_range += tower_placement['range']
        sum_cost += tower_placement['cost']

    return (100*sum_range) - sum_cost

def calculate_avg_fitness(population):
    sum_fitnesses = 0
    for solution in population:
        sum_fitnesses += solution['fitness']

    return sum_fitnesses/len(population)

def crossover(parent_a, parent_b):
    config_a = parent_a['config']
    config_b = parent_b['config']
    crossover_point = math.ceil(len(config_a)/2)

    config_c = np.concatenate((config_a[:crossover_point], config_b[crossover_point:]))
    config_d = np.concatenate((config_b[:crossover_point], config_a[crossover_point:]))

    offspring_c = {'config': config_c, 'fitness': 0}
    offspring_d = {'config': config_d, 'fitness': 0}

    return offspring_c, offspring_d