import csv
import settings as g
import matplotlib.pyplot as plt

'''
OUTPUT IDEAS:
Fitness Progression: best/worst/avg fitness against generation number
Scatter plots of solutions
'''


'''Scatter plot of total range vs total cost where each point is a solution in a population'''
def scatter_plot(population_data, gen_num, evo_stage):
    total_ranges = []
    total_costs = []

    for solution_data in population_data:
        total_ranges.append(int(solution_data[2]))
        total_costs.append(int(solution_data[3]))
    '''
    # Calculate the maximum values for x and y
    max_x = max(total_ranges)
    max_y = max(total_costs)

    # Set the intervals for the axes
    x_interval = max_x / 5  # Adjust the number of intervals as needed
    y_interval = max_y / 5  # Adjust the number of intervals as needed

    plt.scatter(total_ranges, total_ranges, marker='o', color='b')

    # Set the limits and intervals for the x and y axes
    plt.xlim(0, max_x + x_interval)
    plt.ylim(0, max_y + y_interval)
    # Set the ticks for the x and y axes
    plt.xticks(range(0, max_x + 1, x_interval))
    plt.yticks(range(0, max_y + 1, y_interval))'''
    plt.scatter(total_ranges, total_ranges, marker='o', color='b')

    plt.title(f'{gen_num} - {evo_stage}')
    plt.xlabel('Total range')
    plt.ylabel('Total cost')
    plt.show()


if __name__ == '__main__':
    with open(g.output_filename, 'r') as file:
        reader = csv.reader(file)
        population_data = []

        for row in reader:
            # Process each row of data here
            if row[0] == g.title_flag:
                if len(population_data) > 0 and evo_stage != 'TERMINATION':
                    scatter_plot(population_data, gen_num, evo_stage)
                gen_num  = row[1]
                evo_stage = row[2]
                print(f'gathering data for gen {gen_num} after {evo_stage}')
                population_data = []
            else:
                population_data.append(row)


'''
CURRENTLY: only plots 2 attributes - one against the other
=> attributes list must be of size 2
TODO: change
'''
def graph_population(graph_title, population_data, attribute_indexes):
    # TODO: remove this check
    if len(attribute_indexes) != 2:
        raise ValueError('attributes must be of length 2')

    x_attr_index = attribute_indexes[0]
    y_attr_index = attribute_indexes[1]

    x_values = []
    y_values = []

    for solution_data in population_data:
        x_values.append(solution_data[x_attr_index])
        y_values.append(solution_data[y_attr_index])

    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    plt.title('Line Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()



