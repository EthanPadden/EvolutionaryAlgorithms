import csv
import settings as g
import matplotlib.pyplot as plt

'''
OUTPUT IDEAS:
Fitness Progression: best/worst/avg fitness against generation number
TODO: where decimal is the evo stage?
Scatter plots of solutions
'''


'''Scatter plot of total range vs total cost where each point is a solution in a population
THE NUMBER OF GENERATIONS SCATTERED IS LIMITED TO THE AMOUNT OF COLOURS AVAILABLE ON MATPLOTLIB
@:param population_group_data
should be a list with items in the form
[
    gen_num,
    evo_stage,
    population_data
]
'''
def scatter_plot_objective_space(population_group_data):
    '''Gather into this data structure:
    there will be a scatter for each generation
    [
        {
            total_ranges: [...],
            total_costs: [...]
        },
        ...
    ]
    '''
    stats = []
    for entry in population_group_data:
        if len(entry) != 3:
            raise ValueError

        evo_stage = entry[1]
        if evo_stage != 'EVALUATION':
            continue
        population_data = entry[2]

        total_ranges = []
        total_costs = []
        for solution_data in population_data:
            total_ranges.append(solution_data[2])
            total_costs.append(solution_data[3])

        stats.append(
            {
                'total_ranges': total_ranges,
                'total_costs': total_costs
            }
        )

    color_codes = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    handles = []
    labels = []
    for i in range(0, min(len(stats), len(color_codes))):
        scatter = plt.scatter(stats[i]['total_ranges'], stats[i]['total_costs'], marker='o', color=color_codes[i], label=f'{i}')
        handles.append(scatter)
        labels.append(i)
    plt.title('Total ranges vs total cost')
    plt.xlabel('Total range')
    plt.ylabel('Total cost')
    plt.legend(handles, labels)  # Insert legend using handles and labels

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
'''
def line_graph_fitnesses(population_group_data):
    gen_nums = []
    avg_fitnesses = []
    best_fitnesses = []
    worst_fitnesses = []

    for entry in population_group_data:
        if len(entry) != 3:
            raise ValueError

        gen_num = entry[0]
        evo_stage = entry[1]
        if evo_stage != 'EVALUATION':
            continue
        population_data = entry[2]

        fitnesses = []
        total_fitness = 0
        for solution_data in population_data:
            total_fitness += solution_data[1]
            fitnesses.append(solution_data[1])
        avg_fitness = total_fitness/g.population_size
        best_fitnesses.append(max(fitnesses))
        worst_fitnesses.append(min(fitnesses))
        gen_nums.append(gen_num)
        avg_fitnesses.append(avg_fitness)

    plt.plot(gen_nums, avg_fitnesses, marker='o', linestyle='-', color='b', label='avg')
    plt.plot(gen_nums, best_fitnesses, marker='o', linestyle='-', color='g', label='best')
    plt.plot(gen_nums, worst_fitnesses, marker='o', linestyle='-', color='r', label='worst')

    plt.title('Fitnesses')
    plt.xlabel('Generation')
    plt.ylabel('Avg fitness')
    plt.show()

if __name__ == '__main__':
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

        if g.graph_option == 1:
           scatter_plot_objective_space(population_group_data)
        elif g.graph_option == 2:
            line_graph_fitnesses(population_group_data)


