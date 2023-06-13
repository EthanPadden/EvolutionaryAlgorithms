from tabulate import tabulate

import settings as g
class Population:
    def __init__(self, gen_num):
        if gen_num >= g.max_generations:
            raise AttributeError('Max generations reached!')
        else:
            self.__gen_num = gen_num
        self.__solutions = []

    def add_solution(self, solution):
        if len(self.__solutions) < g.population_size:
            self.__solutions.append(solution)
        else:
            raise AttributeError('Population size already met')

    def get_gen_num(self):
        return self.__gen_num

    def to_string(self):
        output = f'gen = {self.__gen_num}'
        table_data = [['bitstring', 'fitness', 'Erange', 'Ecost']]

        for solution in self.__solutions:
            row_data = solution.to_string()
            table_data.append(row_data)

        return tabulate(table_data)

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
