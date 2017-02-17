#!/usr/bin/env python
import sys
import numpy as np
from deap import base, creator, tools
from random import randint

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

class Pizza:

    # Constructor
    def __init__(self, file_name):
        # Load the file and construct the matrix
        self.load_file(file_name)


    # Methods
    def print_info(self):
        print("Rows: " + str(self.number_of_rows))
        print("Columns: " + str(self.number_of_columns))

    def print_results(self):
        print("FINISH THIS")
        #3          3 slices.
        #0021       First slice between rows (0,2) and columns (0,1).
        #0222       Second slice between rows (0,2) and columns (2,2).
        #0324       Third slice between rows (0,2) and columns (3,4).

    def load_file(self, file_name):

        with open(file_name) as file:
            # Read the parameters of the pizza
            header = file.readline().split(' ')
            # and set up the pizza
            self.number_of_rows = int(header[0])
            self.number_of_columns = int(header[1])
            self.minimum_of_each_ingredient_per_slice = int(header[2])
            self.maximum_of_cells_per_slice = int(header[3])

            self.matrix = np.zeros((self.number_of_rows, self.number_of_columns), dtype=np.character)

            i = 0
            # Load the pizza
            for line in file:
                self.matrix[i] = np.array(list(line)[:-1])
                i+=1

    def evaluate(self, individual):

        number_of_mushroms = 0
        number_of_tomatos = 0

        for r in range (individual.r1,individual.r2):
            for c in range (individual.c1,individual.c2):
                if self.matrix[r][c] == 'M':
                    number_of_mushroms += 1
                elif self.matrix[r][c] == 'T':
                    number_of_tomatos += 1

        if number_of_mushroms <= self.minimum_of_each_ingredient_per_slice or number_of_tomatos <= self.minimum_of_each_ingredient_per_slice:
            return -1,

        return sum(individual),

    # generate a random slice
    def generate_rand_slice(self):
        r1 = randint(0, self.number_of_rows-1)
        r2 = randint(r1, self.number_of_rows)
        c1 = randint(0, self.number_of_columns-1)
        c2 = randint(c1, self.number_of_columns)
        return  r1, c1, r2, c2



if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit('Usage: %s <pizza file name>' % sys.argv[0])

    pizza = Pizza(sys.argv[1])
    print(pizza.matrix)


    NGEN = 50
    MU = 50
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2





    IND_SIZE=10





    toolbox = base.Toolbox()
    toolbox.register("attribute", pizza.generate_rand_slice)

    toolbox.register("evaluate", pizza.evaluate)
    # creating types
    creator.create("FitnessMax", base.Fitness, weigths=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)


    # initialize algorithm: invididuals and population

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof)
