import settings as g

def fitness_fn_1(solution):
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
    sum_range, sum_cost = solution.get_totals()
    return g.m*((g.x * sum_range) - (g.y * sum_cost))

def fitness_fn_2(solution):
    # fitness = m * (sum_range/(sum_cost + z))
    # where x is a very small value to account for the edge case where sum_cost = 0
    sum_range, sum_cost = solution.get_totals()
    return g.m*(sum_range/(sum_cost + g.z))


fitness_funtions = [fitness_fn_1, fitness_fn_2]