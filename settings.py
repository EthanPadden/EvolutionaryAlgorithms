'''Problem data'''
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

'''Initialisation variables'''
population_size = 10

'''Evaluation variables'''
# fitness = (x * sum_range) - (y * sum_cost)
x = 100
y = 1

'''Termination criteria variables'''
max_generations = 20
percentage_performance_stagnation = 5

'''Selection variables'''
num_selected_solutions = 6

'''Variation variables'''
crossover = True
mutation = True