import csv
from datetime import datetime

import evolution_stages as evo
import settings as g
from Solution import Solution

if __name__ == '__main__':

    '''Single-objective problem:
    Problem: Optimizing the Placement of Cell Towers for Maximum Coverage
    * Imagine you are a telecommunication company tasked with optimizing the placement of cell towers in a given region to provide maximum coverage and minimize signal interference.
    The objective is to determine the optimal locations for the cell towers to ensure the widest possible coverage while minimizing the number of towers needed.
    * In this problem, you are provided with a map of the region and need to decide where to place the cell towers.
    Each potential tower location has associated coverage radius and cost.
    The coverage radius determines the area in which the tower can provide reliable signal strength.
    The cost represents the expense of installing and maintaining the tower.
    * The goal is to find the optimal set of tower locations that maximizes the coverage area while minimizing the total cost of installation and maintenance.
    '''
    # Lets say we have a fixed number T of possible tower locations (easier to zero index)
    # [t0, t1, ..., tT]
    # Each solution will be a configuration of tower placements out of the possible T tower placements
    # Each tower placement has an associated radius and cost
    # We want to maximise radius while minimising cost
    # This does not take signal interference or overlap into account TODO: ?

    # Solution representation:
    # configuration consists of 3 towers
    # since each tower location is at a set index, we can use a bitstring of length T
    # e.g. if T = 8 config [t2, t5, t6] can be represented as 00100110
    # solution: { bitstring : fitness }
    # population consists of N possible tower configurations
    with open(g.input_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            Solution.possible_tower_placements.append(
                {
                    'range': int(row[0]),
                    'cost': int(row[1])
                }
            )

    output_filename = f"output/output {datetime.now().strftime('Y-%m-%d_%H-%M-%S.csv')}"

    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)

        # INITIALISATION    ===================================
        current_gen = evo.initialise()
        writer.writerow(['STAGE', 'INITIALISATION'])
        writer.writerows(current_gen.to_csv())

        # GENERATIONAL LOOP
        prev_avg_fitness = 0

        while (True):
            writer.writerow(['GEN', current_gen.get_gen_num()])

            # EVALUATION        ===================================
            evo.evaluate(current_gen)
            writer.writerow(['STAGE', 'EVALUATION'])
            writer.writerows(current_gen.to_csv())

            # TERMINATION       ===================================
            # In this problem, we don't have an ideal fitness if we can improve the cost-range tradeoff
            # So no fitness condition

            # Max generations reached?
            writer.writerow(['STAGE', 'TERMINATION'])

            if current_gen.get_gen_num() >= g.max_generations:
                writer.writerow(['max gens', 'true', 'terminate', 'true'])
                break
            writer.writerow(['max gens', 'false', 'terminate', 'false'])

            # Performance stagnation?
            # Instead of a threshold value, we can take this as a percentage
            # ie if we don't see an increase of at least 5% for the average fitness, stop
            current_avg_fitness = current_gen.calc_avg_fitness()
            diff_avg_fitness = current_avg_fitness - prev_avg_fitness
            if (current_gen.get_gen_num() > 0):
                if ((diff_avg_fitness / prev_avg_fitness) * 100) < 5:
                    writer.writerow(['perf stagn', 'true', current_avg_fitness, prev_avg_fitness, diff_avg_fitness])
                    break
            writer.writerow(['perf stagn', 'false', 'terminate', 'false'])

            # SELECTION       ===================================
            if g.selection_method == g.SelectionMethod.FITNESS:
                next_gen = evo.select_by_sorting(current_gen)
            elif g.selection_method == g.SelectionMethod.DOMINANCE:
                next_gen = evo.select_by_examining_dominance_relationships(current_gen)
            writer.writerow(['STAGE', 'SELECTION'])
            writer.writerows(current_gen.to_csv())

            # # VARIATION       ===================================
            evo.variation(current_gen, next_gen)
            writer.writerow(['STAGE', 'VARIATION'])
            writer.writerows(current_gen.to_csv())

            prev_avg_fitness = current_avg_fitness
            current_gen = next_gen
            # TODO: dont create output file unless no errors occurred - catch exception and delete file
