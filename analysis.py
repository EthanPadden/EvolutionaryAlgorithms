import csv
import settings as g
import matplotlib.pyplot as plt

'''
OUTPUT IDEAS:
Fitness Progression: best/worst/avg fitness against generation number
TODO: where decimal is the evo stage?
Scatter plots of solutions
'''


'''Scatter plot of total range vs total cost where each point is a solution in a population'''
def scatter_plot(population_data, gen_num, evo_stage):
    total_ranges = []
    total_costs = []

    for solution_data in population_data:
        total_ranges.append(int(solution_data[2]))
        total_costs.append(int(solution_data[3]))

    plt.scatter(total_ranges, total_ranges, marker='o', color='b')
    plt.title(f'{gen_num} - {evo_stage}')
    plt.xlabel('Total range')
    plt.ylabel('Total cost')
    plt.show()

'''
@:param population_group_data
should be a list with items in the form
[
    gen_num,
    evo_stage,
    population_data
]

Line graph of fitness (best/worst/avg) against generation number
TODO: best and worst fitness not just avg
'''
def line_graph_fitnesses(population_group_data):
    gen_nums = []
    avg_fitnesses = []
    for entry in population_group_data:
        if len(entry) != 3:
            raise ValueError

        gen_num = entry[0]
        evo_stage = entry[1]
        if evo_stage != 'EVALUATION':
            continue
        population_data = entry[2]

        total_fitness = 0
        for solution_data in population_data:
            total_fitness += solution_data[1]
        avg_fitness = total_fitness/g.population_size

        gen_nums.append(gen_num)
        avg_fitnesses.append(avg_fitness)

    plt.plot(gen_nums, avg_fitnesses, marker='o', linestyle='-', color='b')
    plt.title('Average fitnesses')
    plt.xlabel('Generation')
    plt.ylabel('Avg fitness')
    plt.show()

if __name__ == '__main__':
    if g.graph_option == 1:
        # TODO: update for new output format
        pass
        # with open(g.output_filename, 'r') as file:
        #     reader = csv.reader(file)
        #     population_data = []
        #
        #     for row in reader:
        #         # Process each row of data here
        #         if row[0] == g.title_flag:
        #             if len(population_data) > 0 and evo_stage != 'TERMINATION':
        #                 scatter_plot(population_data, gen_num, evo_stage)
        #             gen_num  = row[1]
        #             evo_stage = row[2]
        #             print(f'gathering data for gen {gen_num} after {evo_stage}')
        #             population_data = []
        #         else:
        #             population_data.append(row)
    elif g.graph_option == 2:
        with open(g.output_filename, 'r') as file:
            reader = csv.reader(file)
            current_gen_num = -1
            population_data = []
            population_group_data = []
            evo_stage = None
            row = next(reader, None)
            while row is not None:
                if row[0] == 'GEN':
                    # Check and update gen num
                    next_gen_num = int(row[1])
                    if next_gen_num == current_gen_num:
                        # We are still processing this generation
                        # The next line should be the evaluation stage data
                        row = next(reader, None)
                        if row[1] != 'EVALUATION':
                            raise ValueError
                    elif next_gen_num == (current_gen_num + 1):
                        # We are processing the next generation
                        current_gen_num += 1
                        pass
                    else:
                        # This situation should not happen
                        raise ValueError(f'{current_gen_num} => {next_gen_num}')
                elif row[0] == 'STAGE':
                    population_group_data.append(
                        [
                            current_gen_num,
                            evo_stage,
                            population_data
                        ]
                    )

                    evo_stage = row[1]
                    population_data = []
                else:
                    processed_row = []
                    for gene in row:
                        if gene == '':
                            processed_row.append(None)
                        if gene.isdigit():
                            processed_row.append(int(gene))
                        elif gene.count('.') == 1 and gene.replace('.', '').isdigit():
                            processed_row.append(float(gene))
                    population_data.append(processed_row)

                row = next(reader, None)
            population_group_data.pop(0)
            line_graph_fitnesses(population_group_data)

