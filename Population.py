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