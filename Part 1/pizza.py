import sys
import numpy as np
from deap import base, creator, tools
from random import randint

from math import ceil

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

            self.bool_matrix = np.full((self.number_of_rows, self.number_of_columns), False, dtype=np.bool)

            i = 0
            # Load the pizza
            for line in file:
                self.matrix[i] = np.array(list(line)[:-1])
                i+=1

    def evaluate(self, individual):

        pizza_points = 0

        for item in individual:

            slice_points = 0

            number_of_mushroms = 0
            number_of_tomatos = 0

            for r in range(item[0],item[2]+1):
                for c in range (item[1],item[3]+1):
                    if self.matrix[r, c] == 'M':
                        number_of_mushroms += 1
                    elif self.matrix[r, c] == 'T':
                        number_of_tomatos += 1

            if number_of_mushroms >= self.minimum_of_each_ingredient_per_slice and number_of_tomatos >= self.minimum_of_each_ingredient_per_slice:
                slice_points = sum(item)

            pizza_points += slice_points


        return pizza_points,

    # generate a random slice
    def generate_rand_slice(self):
        nelems = np.Infinity
        have_enough_ingrs = False
        not_taken = True
        while nelems > self.maximum_of_cells_per_slice and not have_enough_ingrs\
                and not_taken:
            r1 = randint(0, self.number_of_rows - 2)
            r2 = randint(r1 + 1, self.number_of_rows - 1)
            c1 = randint(0, self.number_of_columns - 2)
            c2 = randint(c1 + 1, self.number_of_columns - 1)
            # check the slice generated is not bigger than maximum size
            nrows = (r2 - r1) + 1
            ncols = (c2 - c1) + 1
            nelems = nrows * ncols

            n_tomatos = len(np.where(self.matrix[r1:r2+1, c1:c2+1] == 'T'))
            n_mushroms = len(np.where(self.matrix[r1:r2, c1:c2] == 'M'))

            if n_mushroms >= self.minimum_of_each_ingredient_per_slice and \
                            n_tomatos >= self.minimum_of_each_ingredient_per_slice:
                have_enough_ingrs = True

            if np.any(self.bool_matrix[r1:r2+1, c1:c2+1]):
                not_taken = False

        self.bool_matrix[r1:r2+1, c1:c2+1] = True

        return r1, c1, r2, c2


    def mutate(self, individual):

        contract = randint(0,3)
        slice = randint(0, len(individual)-1)

        print("contract = ", contract, " slice = ", slice)

        if contract == 0:
            # Eliminate the upper row of the slice
            self.bool_matrix[individual[slice][0], individual[slice][1]:individual[slice][3]+1] = False
            a, b, c, d = individual[slice]
            individual[slice] = (a+1, b, c, d)

        elif contract == 2:
            # Eliminate the left column of the slice
            self.bool_matrix[individual[slice][0]:individual[slice][2] + 1, individual[slice][1]] = False
            a, b, c, d = individual[slice]
            individual[slice] = (a, b+1, c, d)

        elif contract == 3:
            # Eliminate the last row of the slice
            self.bool_matrix[individual[slice][2], individual[slice][1]:individual[slice][3] + 1] = False
            a, b, c, d = individual[slice]
            individual[slice] = (a, b, c-1, d)

        elif contract == 4:
            # Eliminate the right column of the slice
            self.bool_matrix[individual[slice][0]:individual[slice][2] + 1, individual[slice][3]] = False
            a, b, c, d = individual[slice]
            individual[slice] = (a, b, c, d-1)

        return individual,

if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit('Usage: %s <pizza file name>' % sys.argv[0])

    pizza = Pizza(sys.argv[1])
    # print(pizza.matrix)

    # creating types
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # initialize algorithm: invididuals and population
    IND_INIT_SIZE=ceil(pizza.matrix.size/pizza.maximum_of_cells_per_slice)
    toolbox = base.Toolbox()
    toolbox.register("attribute", pizza.generate_rand_slice)
    toolbox.register("individual", tools.initRepeat, creator.Individual, 
                     toolbox.attribute, IND_INIT_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", pizza.evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", pizza.mutate)
    toolbox.register("select", tools.selBest) # use the pre-set operators
    #toolbox.register("select", tools.selNSGA2) # use the pre-set operators

    population = toolbox.population(n=100)
    algorithms.eaSimple(population, toolbox, cxpb=0.75, mutpb=0.05, ngen=50)

