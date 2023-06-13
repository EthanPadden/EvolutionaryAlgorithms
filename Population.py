from tabulate import tabulate

import settings as g
class Population:
    def __init__(self, gen_num):
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