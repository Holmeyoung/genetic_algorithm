import numpy as np
import matplotlib.pyplot as plt
import random
random.seed(0)

# Decode
def decode_convert(binary):
    return -1 + (int(binary, 2) / int('1111111111111111111111', 2)) * 3

# Given genes, value the adaptability of individual.
def adaptability(genes):
    # Here, gene is only the location of axis x. The gene is expressed in binary mode
    x = decode_convert(genes)
    return x * np.sin(10 * np.pi * x) + 2

# Roulette. Given a number of individuals, choose one according to their adaptability.
def roulette(population):
    # According to the adaptability to calculate the percent of each one
    sum = 0
    for value in population.values():
        sum += value
    population_percent = {}

    # Calculate the interval of each individual
    bgain = 0
    end = 0
    for key, value in population.items():
        end = bgain + value/sum
        population_percent[key] = [bgain, end]
        bgain = end
    
    # Turn the turntable
    r = random.random()
    for key, value in population_percent.items():
        if r > population_percent[key][0] and r < population_percent[key][1]:
            return key

# Use roulette to choose a certain ratio individuals from all.
def select(ratio, top_n_to_keep, population):
    population_select = {}
    population_list = sorted(population.items(), key = lambda x: x[1], reverse = True)
    for i in range(min(top_n_to_keep, len(population)*ratio)):
        key = population_list[i][0]
        value = population_list[i][1]
        population_select[key] = value

    while (len(population_select) < len(population)*ratio):
        key = roulette(population)
        population_select[key] = population[key]

    return population_select

# Chromosome crossing
def crossover(rate, population):
    key1 = roulette(population) # key1 is the base.Because the higher adaptability, the higher possibility to be chosen frist. 
    key2 = key1
    while (key2 == key1):
        key2 = roulette(population)
    key = ''
    for i, j in zip(key1, key2):
        r = random.random()
        new = i
        if r < rate:
            new = j
        key += new
    return key

# Chromosomal variation
def mutation(rate, population):
    key1 = roulette(population)
    key = ''
    for i in key1:
        r = random.random()
        new = i
        if r < rate:
            new = str(1 - int(i))
        key += new
    return key

# Show the figure
def show(population, x, y):
    points_x = []
    points_y = []
    for key, value in population.items():
        points_x.append(decode_convert(key))
        points_y.append(value)
    
    plt.cla()
    plt.plot(x, y)
    plt.scatter(points_x, points_y, alpha=0.6, color = 'r')
    plt.pause(2)

# Population init
def init_population(population_number):
    population = {}
    while (len(population) < population_number):
        dec = random.randint(0, int('1111111111111111111111', 2))
        # bin(4): 0b100
        key = bin(dec)[2:]
        population[key] = adaptability(key)
    
    return population

# Main process function
def main_process(select_ratio, top_n_to_keep, epoch, population_number, x, y, crossover_possi, mutation_possi):
    population = init_population(population_number)

    for i in range(epoch):
        show(population, x, y)
        population_select = select(select_ratio, top_n_to_keep, population)
        population = dict(population_select)
        while (1):
            key_crossover = crossover(crossover_possi, population_select)
            population[key_crossover] = adaptability(key_crossover)
            if len(population) >= population_number:
                break

            key_mutation = mutation(mutation_possi, population_select)
            population[key_mutation] = adaptability(key_mutation)
            if len(population) >= population_number:
                break


if __name__ == "__main__":
    # Function image
    x_ori = np.arange(-1.0, 2.0, 0.01)
    y_ori = x_ori * np.sin(10 * np.pi * x_ori) + 2

    # Params
    population_number = 55 # Number of population
    select_ratio = 0.7 # Keep ratio every generation when select
    top_n_to_keep = 3 # When select, keep top n
    epoch = 50 # Generation number
    crossover_possi = 0.6 # Possibility of chromosome crossing
    mutation_possi = 0.01 # Possibility of chromosomal variation

    main_process(select_ratio, top_n_to_keep, epoch, population_number, x_ori, y_ori, crossover_possi, mutation_possi)
