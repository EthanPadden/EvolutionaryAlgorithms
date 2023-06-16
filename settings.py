'''IO settings'''
input_filename = 'input/input 1.csv'
output_filename = 'output/output Y-06-16_09-12-44.csv'
# Available graphs:
#   1 - Scatter plot of total range vs total cost where each point is a solution in a population
#   2 - Line graph of fitness (best/worst/avg) against generation number
graph_option = 1

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