import math
import random
import copy
import numpy as np


class Attraction:
    def __init__(self, index, referTime, timeWindow, referCost, name, information):
        self.index = index
        self.referTime = referTime
        self.timeWindow = timeWindow
        self.referCost = referCost
        self.name = name
        self.information = information


class Hotel:
    def __init__(self, index, name, expenses):
        self.index = index
        self.name = name
        self.expenses = expenses


class Chromosome:
    def __init__(self, hotel_index: int, attraction_order: list, subwayOrTaxi: list):
        self.hotel_index = hotel_index
        self.attraction_order = attraction_order
        self.subwayOrTaxi = subwayOrTaxi  # 0 means subway, 1 means taxi

        self.order = []
        self.days = 0
        self.time = 0
        self.cost = 0

def getRandomDecimal():
    return random.uniform(0, 1)


class TravelPlanner:
    def __init__(self, attractions, hotels, subwayTimeTable_a, subwayCostTable_a, taxiTimeTable_a, taxiCostTable_a,
                 subwayTimeTable_h, subwayCostTable_h, taxiTimeTable_h, taxiCostTable_h):
        """
        :param attractions:
        :param hotels:
        :param subwayTimeTable_a: among attractions
        :param subwayCostTable_a: among attractions
        :param taxiTimeTable_a: among attractions
        :param taxiCostTable_a: among attractions
        """
        self.attractions = attractions
        self.hotels = hotels

        self.subwayTimeTable_a = subwayTimeTable_a
        self.subwayCostTable_a = subwayCostTable_a
        self.taxiTimeTable_a = taxiTimeTable_a
        self.taxiCostTable_a = taxiCostTable_a

        self.subwayTimeTable_h = subwayTimeTable_h
        self.subwayCostTable_h = subwayCostTable_h
        self.taxiTimeTable_h = taxiTimeTable_h
        self.taxiCostTable_h = taxiCostTable_h

        self.dailyTimeLimit = 14

        # EA parameters
        self.nGeneration = 100
        self.nPopulation = 50
        self.crossoverRate = 0.8
        self.mutationRate = 0.8
        self.randomSeed = 0

    def optimize(self):
        # Implement the optimization algorithm using Evolutionary Algorithm
        """
        1. Encoding: [hotel_index, attraction list, transportation choice]
            hotel index: specify which hotel our algorithm choose to live
            attraction list: specify what order our algorithm choose to visit
            transportation choice: choose to take subway or taxi
        ---------------------------------------------------------------------------
        2. Initialization

        ---------------------------------------------------------------------------
        3. Evaluation

        ---------------------------------------------------------------------------
        4. Crossover

        ---------------------------------------------------------------------------
        5. Mutation

        ---------------------------------------------------------------------------
        6. Selection

        ---------------------------------------------------------------------------
        :return:
        """
        random.seed(0)
        # 2. Initialization
        population = self.initialization()
        # ---------------------------------------------------------------------------
        avg_record = []
        best_record = []

        # HaHaHaHa, Holy Evolutionary Algorithm BEGINS!!!!!!!!!
        for _ in range(self.nGeneration):
            # 3. Evaluation
            population.sort(key=lambda x: self.evaluation(x))  # Rank the population in ascending order
            # print("a: " + str(self.evaluation(population[0])))
            # ---------------------------------------------------------------------------
            # 6. Selection Parent for Crossover
            parents = self.generateParents(population, self.nPopulation)
            # ---------------------------------------------------------------------------
            # 4. Crossover
            offsprings = []
            for i in range(math.floor(self.nPopulation / 2)):
                [child1, child2] = self.crossover(parents[2 * i], parents[2 * i + 1])
                offsprings.append(child1)
                offsprings.append(child2)
            # ---------------------------------------------------------------------------
            # 5. Mutation
            mutated_offsprings = []
            for offspring in offsprings:
                mutated_offsprings.append(self.mutation(offspring))

            population = population + mutated_offsprings
            # ---------------------------------------------------------------------------
            # print("b: " + str(self.evaluation(population[0])))
            # 6. Selection Next Generation
            population.sort(key=lambda x: self.evaluation(x))
            population = population[0:self.nPopulation]

            # To record the fitness of each generation
            fitness = [self.evaluation(x) for x in population]

            avg_fitness = np.mean(fitness)
            best_fitness = np.min(fitness)
            # print("Generation: " + str(_))
            # print("Best Fitness: " + str(best_fitness))
            avg_record.append(avg_fitness)
            best_record.append(best_fitness)
        # Return the best solution found
        best_individual = min(population, key=lambda x: self.evaluation(x))
        return [best_individual, best_record, avg_record]
        pass

    def initialization(self):
        population = []
        for _ in range(self.nPopulation):
            hotel_index = random.randint(0, len(self.hotels) - 1)  # randomly select a hotel index from the hotels list
            attraction_order = [x for x in range(len(self.attractions))]
            random.shuffle(attraction_order)  # generate random order of attractions

            rows = len(self.hotels) + len(self.attractions)
            cols = len(self.hotels) + len(self.attractions)
            subwayOrTaxi = [[0] * cols for _ in range(rows)]
            for i in range(rows):
                for j in range(cols):
                    subwayOrTaxi[i][j] = random.choice([0, 1])

            individual = Chromosome(hotel_index, attraction_order, subwayOrTaxi)
            population.append(individual)
        return population

    def evaluation(self, individual: Chromosome):
        Time = 0  # Minimization Objective in seconds
        Cost = 0  # Minimization Objective
        order = [-(individual.hotel_index+1)]

        aggregateTime = 0  # accumulated time in one day
        vertexIndex = individual.hotel_index  # pointer to which vertex traveler are visiting, default to be at hotel chosen by individual
        days = 1

        i = 0
        while i < len(individual.attraction_order):
            attraction_index = individual.attraction_order[i]
            # foreach attraction in attraction order made by individual

            attraction = self.attractions[attraction_index]  # get the attraction object by its index
            referTime = attraction.referTime
            referCost = attraction.referCost
            attractionIndex = attraction_index  # for further cost and time calculation

            # decide take taxi or subway
            taking_taxi = individual.subwayOrTaxi[vertexIndex][len(self.hotels) + attractionIndex]

            if aggregateTime + referTime < self.dailyTimeLimit:  # if add this attraction to today's routine will not surpass the time limit for one day
                # go from 'vertexIndex' to 'attractionIndex'
                order.append(attractionIndex)

                if aggregateTime == 0:  # A new day begins
                    # Calculate Time
                    transportationTime = self.taxiTimeTable_h[vertexIndex][attractionIndex] if taking_taxi else \
                        self.subwayTimeTable_h[vertexIndex][attractionIndex]

                    # Calculate Cost
                    transportationCost = self.taxiCostTable_h[vertexIndex][attractionIndex] if taking_taxi else \
                        self.subwayCostTable_h[vertexIndex][attractionIndex]
                    Cost += (transportationCost + referCost)
                else:  # vertex is not in hotel
                    # Calculate Time
                    transportationTime = self.taxiTimeTable_a[vertexIndex][attractionIndex] if taking_taxi else \
                        self.subwayTimeTable_a[vertexIndex][attractionIndex]

                    # Calculate Cost
                    transportationCost = self.taxiCostTable_a[vertexIndex][attractionIndex] if taking_taxi else \
                        self.subwayCostTable_a[vertexIndex][attractionIndex]

                # You have arrived at attractionIndex
                aggregateTime += (transportationTime + referTime)  # update aggregate time
                Time += transportationTime
                Cost += transportationCost
                vertexIndex = attractionIndex
                i = i + 1

            else:  # else change to next day
                hotel_index = individual.hotel_index
                order.append(-(hotel_index+1))
                Time += self.taxiTimeTable_h[hotel_index][vertexIndex] if taking_taxi else \
                    self.subwayTimeTable_h[hotel_index][vertexIndex]
                Cost += self.taxiCostTable_h[hotel_index][vertexIndex] if taking_taxi else \
                    self.subwayCostTable_h[hotel_index][vertexIndex]

                aggregateTime = 0
                days = days + 1
                vertexIndex = hotel_index

        individual.order = order
        individual.days = days
        individual.time = Time
        individual.cost = Cost
        return Time + Cost

    def crossover(self, individual1: Chromosome, individual2: Chromosome):
        child1 = copy.copy(individual1)
        child2 = copy.copy(individual2)

        # Crossover hotel index
        if random.uniform(0, 1) < self.crossoverRate:
            temp = child1.hotel_index
            child1.hotel_index = child2.hotel_index
            child2.hotel_index = temp

        # Crossover attraction order
        if random.uniform(0, 1) < self.crossoverRate:
            order1 = copy.copy(child1.attraction_order)
            order2 = copy.copy(child2.attraction_order)

            ptr = random.randint(1, len(self.attractions))  # Cutting point
            new_order1 = order1[0:ptr]
            for e in order2:
                if e not in new_order1:
                    new_order1.append(e)

            new_order2 = order2[0:ptr]
            for e in order1:
                if e not in new_order2:
                    new_order2.append(e)

            child1.attraction_order = new_order1
            child2.attraction_order = new_order2

        # Crossover subwayOrTaxi
        if random.uniform(0, 1) < self.crossoverRate:
            rows = len(self.hotels) + len(self.attractions)
            cols = len(self.hotels) + len(self.attractions)
            matrix1 = [[0] * cols for _ in range(rows)]
            matrix2 = [[0] * cols for _ in range(rows)]
            for r in range(rows):
                for c in range(cols):
                    if random.uniform(0, 1) < 0.5:
                        matrix1[r][c] = child1.subwayOrTaxi[r][c]
                        matrix2[r][c] = child2.subwayOrTaxi[r][c]
                    else:
                        matrix2[r][c] = child1.subwayOrTaxi[r][c]
                        matrix1[r][c] = child2.subwayOrTaxi[r][c]
            child1.subwayOrTaxi = matrix1
            child2.subwayOrTaxi = matrix2
        return child1, child2

    def mutation(self, individual: Chromosome):
        child = copy.copy(individual)
        # Mutate hotel index:
        if getRandomDecimal() < self.mutationRate:
            child.hotel_index = random.randint(0, len(self.hotels) - 1)

        # Mutate attraction order:
        if getRandomDecimal() < self.mutationRate:
            random.shuffle(child.attraction_order)

        # Mutate subwayOrTaxi:
        if getRandomDecimal() < self.mutationRate:
            rows = len(self.hotels) + len(self.attractions)
            cols = len(self.hotels) + len(self.attractions)
            for r in range(rows):
                for c in range(cols):
                    if getRandomDecimal() < self.mutationRate:
                        child.subwayOrTaxi[r][c] = (child.subwayOrTaxi[r][c] + 1) % 2

        return child

    def generateParents(self, population, nParents):
        parents = []
        # Generate selection probability
        probability = [1 / self.evaluation(x) for x in population]
        total_probability = sum(probability)
        normalized_probability = [x / total_probability for x in probability]

        for i in range(1, len(normalized_probability)):
            normalized_probability[i] += normalized_probability[i - 1]

        for _ in range(nParents):
            r = random.uniform(0, 1)
            for index in range(len(normalized_probability)):
                if r < normalized_probability[index]:
                    parents.append(copy.deepcopy(population[index]))
                    break

        return parents
