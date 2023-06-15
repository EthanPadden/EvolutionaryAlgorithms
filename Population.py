import random

from tabulate import tabulate

import settings as g
class Population:
    def __init__(self, gen_num):
        if gen_num >= g.max_generations:
            raise AttributeError('Max generations reached!')
        else:
            self.__gen_num = gen_num
        self.__solutions = []


    def clear_solutions(self):
        self.__solutions = []

    def add_solution(self, solution):
        if len(self.__solutions) < g.population_size:
            self.__solutions.append(solution)
        else:
            raise AttributeError('Population size already met')

    def get_gen_num(self):
        return self.__gen_num

    def to_string(self):
        table_data = [['bitstring', 'fitness', 'Erange', 'Ecost']]

        for solution in self.__solutions:
            row_data = solution.to_string()
            table_data.append(row_data)

        return tabulate(table_data)

    def to_csv(self):
        rows = []
        for solution in self.__solutions:
            row_data = solution.to_csv()
            rows.append(row_data)
        return rows

    def get_solutions(self):
        return self.__solutions

    def get_gen_num(self):
        return self.__gen_num

    def calc_avg_fitness(self):
        sum_fitnesses = 0
        for solution in self.__solutions:
            sum_fitnesses += solution.get_fitness()

        return sum_fitnesses / g.population_size

    def sort(self):
        # Sort the population by fitness
        sorted_solutions = sorted(self.__solutions, key=lambda solution: solution.get_fitness())
        self.__solutions = sorted_solutions

    def mutate(self):
        # choose a random number of solutions
        num_solutions_to_mutate = random.randint(1, g.population_size)
        for i in range(1, num_solutions_to_mutate):
            # choose a random solution

            soln_index_to_mutate = random.randint(0, (g.population_size - 1))
            soln_to_mutate = self.__solutions[soln_index_to_mutate]

            # choose a random number of bits to flip
            num_bits_to_flip = random.randint(0, (len(g.possible_tower_placements) - 1))

            for i in range(0, num_bits_to_flip):
                # choose a random bit and flip it
                bit_index_to_flip = random.randint(0, (len(g.possible_tower_placements) - 1))
                config = soln_to_mutate.get_config()
                if config[bit_index_to_flip] == 0:
                    config[bit_index_to_flip] = 1
                elif config[bit_index_to_flip] == 1:
                    config[bit_index_to_flip] = 0
                else:
                    raise ValueError
                soln_to_mutate.set_config(config)
                # TODO: more efficient way
