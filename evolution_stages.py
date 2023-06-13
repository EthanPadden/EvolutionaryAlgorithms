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

def select(current_gen):
    # Sort the population by fitness
    sorted_population = sorted(current_gen, key=lambda x: x['fitness'], reverse=True)
    next_gen = []
    for i in range(0, g.num_selected_solutions):
        next_gen.append(sorted_population[i])

    return next_gen