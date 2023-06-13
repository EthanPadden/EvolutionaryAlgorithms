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