import settings as g
class Solution:
    def __init__(self, config):
        self.__config = config
        self.__fitness = None

    def to_string(self):
        bitstring = ''.join(map(str, self.__config))

        tower_placements = []
        for i in range(0, len(self.__config)):
            if self.__config[i] == 1:
                tower_placements.append(g.possible_tower_placements[i])
            elif self.__config[i] != 0:
                raise ValueError

        total_range = 0
        total_cost = 0
        for tower_placement in tower_placements:
            total_range += tower_placement['range']
            total_cost += tower_placement['cost']

        # TODO: change to tabulate
        # TODO: change so that tower placements stats are stored rather than calculated every time to_string is called
        return [
            bitstring,
            self.__fitness,
            total_range,
            total_cost
        ]


    def calc_fitness(self):
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
        for i in range(0, len(self.__config)):
            if self.__config[i] == 1:
                tower_placements.append(g.possible_tower_placements[i])
            elif self.__config[i] != 0 and self.__config[i] != 1:
                raise ValueError

        # Sum the variables in this solution
        sum_range = 0
        sum_cost = 0
        for tower_placement in tower_placements:
            sum_range += tower_placement['range']
            sum_cost += tower_placement['cost']

        self.__fitness = (100 * sum_range) - sum_cost

    def get_fitness(self):
        return self.__fitness

    def get_config(self):
        return self.__config

    def set_config(self, config):
        self.__config = config