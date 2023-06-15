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
# m is a multiplier that should not affect the fitness, just makes it easier for analysis
m = 1000

fitness_fn_num = 2
# fitness_fn_1 = m * ((x * sum_range) - (y * sum_cost))
x = 1
y = 1
# fitness_fn_2 = m * (sum_range/(sum_cost + z))
z = 0.000001

'''Termination criteria variables'''
max_generations = 20
percentage_performance_stagnation = 5

'''Selection variables'''
num_selected_solutions = 6

'''Variation variables'''
crossover = True
mutation = True