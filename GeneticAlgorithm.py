import random

class Individual:
    def __init__(self, genome: list):
        self.genome = genome
        self.num_genes = len(self.genome)
        self.fitness = 0.0

    def get_genome(self):
        return self.genome

    def get_genome_length(self):
        return self.num_genes

    def get_fitness(self):
        return self.fitness

    def gene_at(self, index):
        return self.genome[index]

    def calculate_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self._distance())
        return self.fitness

    def mutate(self, mutation_rate):
        '''
        Randomly swap two genes
        Will be applied on the offsprings from crossover
        '''
        if mutation_rate <= 0:
            return
        for gene1 in range(self.num_genes):
            if random.random() < mutation_rate:
                gene2 = int(random.random() * self.num_genes)
                self.genome[gene1], self.genome[gene2] = self.genome[gene2], self.genome[gene1]

    def _distance(self):
        distance = 0
        for i in range(0, self.num_genes):
            src = self.genome[i]
            dest = None
            if i+1 < self.num_genes:
                dest = self.genome[i+1]
            else:
                dest = self.genome[0]
            distance += src.distance(dest)
        return distance


class Population:
    def __init__(self, individuals=None):
        if individuals == None:
            self.gene_list = []
            self.individuals = []
            self.num_members = 0
        else:
            self.gene_list = individuals[0].get_genome()
            self.individuals = individuals
            self.num_members = len(individuals)

    def initialize_population(self, gene_list, size):
        self.gene_list = gene_list
        self.num_members = size
        for _ in range(0, size):
            genome = random.sample(gene_list, len(gene_list))
            self.individuals.append(Individual(genome))

    def get_num_members(self):
        return self.num_members

    def get_individual(self, index) -> Individual:
        return self.individuals[index]

    def get_fittest(self) -> Individual:
        return max(self.individuals, key=lambda ind: ind.calculate_fitness())

    def ranking(self):
        fitness_results = []
        for i in range(0, self.num_members):
            fitness = self.get_individual(i).calculate_fitness()
            fitness_results.append((i, fitness))
        return sorted(fitness_results, key=lambda tup: tup[1], reverse=True)

    def grow(self, size):
        self.num_members += size
        for _ in range(0, size):
            genome = random.sample(self.gene_list, len(self.gene_list))
            self.individuals.append(Individual(genome))

    def combine(self, population2: 'Population'):
        self.individuals.extend(population2.individuals[:int(population2.get_num_members()/2)])
        return Population(self.individuals)


class GAResults:
    def __init__(self, population: Population, progress) -> None:
        self.population = population
        self.fittest_individual = population.get_fittest()
        self.progress = progress
    
    def fittest_genome(self) -> list:
        return self.fittest_individual.get_genome()

    def best_fitness(self) -> float:
        return self.fittest_individual.get_fitness()

    def get_progress(self) -> list:
        return self.progress

    def get_whole_population(self) -> Population:
        return self.population


class GA:
    def __init__(self, gene_list, pop_size=100, elite_size=20, mutation_rate=0.5, generations=500, pop_growth=False, early_stop=50):
        self.population = Population()
        self.population.initialize_population(gene_list, pop_size)
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.pop_growth = pop_growth
        self.early_stop_rounds = early_stop
        self.progress = []
        self.best_fitness_score = 0
        self.best_generation = 0

    def execute(self) -> GAResults:
        # First round
        for i in range(0, self.generations):
            self.next_generation(i)
            if (self.early_stop_rounds != -1 and self.early_stop(i)):
                break

        if self.pop_growth:
            # Second round: population growth
            growth_size = int(self.population.get_num_members() * 0.25)
            self.population.grow(growth_size)
            for i in range(0, self.generations):
                self.next_generation(i)
                if (self.early_stop_rounds != -1 and self.early_stop(i)):
                    break

            # Third round: population growth
            growth_size = int(self.population.get_num_members() * 0.25)
            self.population.grow(growth_size)
            for i in range(0, self.generations):
                self.next_generation(i)
                if (self.early_stop_rounds != -1 and self.early_stop(i)):
                    break

            # Fourth round: population growth
            growth_size = int(self.population.get_num_members() * 0.25)
            self.population.grow(growth_size)
            for i in range(0, self.generations):
                self.next_generation(i)
                if (self.early_stop_rounds != -1 and self.early_stop(i)):
                    break

        return GAResults(self.population, self.progress)

    def next_generation(self, generation):
        rank_list = self.population.ranking()
        self.record_progress(generation, rank_list[0][1])
        mating_pool = self.create_mating_pool(rank_list)
        children = self.breed(mating_pool)
        self.population = self.new_population(children)
        # self.mutation_rate /= 2

    def new_population(self, individuals):
        population = Population(individuals)
        return population

    def create_mating_pool(self, rank_list):
        mating_pool = []
        for selection in self.selection(rank_list):
            mating_pool.append(self.population.get_individual(selection))
        return mating_pool

    def selection(self, rank_list):
        '''
        Roulette Wheel Selection
        '''
        selections = []

        for i in range(0, self.elite_size):
            selections.append(rank_list[i][0])

        max = sum([rank[1] for rank in rank_list])
        for _ in range(0, len(rank_list)-self.elite_size):
            pick = random.uniform(0, max)
            cum_sum = 0
            for rank in rank_list:
                cum_sum += rank[1]
                if pick <= cum_sum:
                    selections.append(rank[0])
                    break
        return selections

    def breed(self, mating_pool):
        children = []
        pool = random.sample(mating_pool, len(mating_pool))

        for i in range(0, self.elite_size):
            children.append(mating_pool[i])

        for i in range(0, len(mating_pool)-self.elite_size):
            child = self.crossover(pool[i], pool[len(mating_pool)-i-1])
            children.append(child)
        return children

    def crossover(self, parent1: Individual, parent2: Individual):
        left, right = [], []
        genome_length = parent1.get_genome_length()

        parent1_portion = parent1.get_fitness() / (parent1.get_fitness()+parent2.get_fitness())
        start_gene = min(int(random.random()*genome_length), int(random.random()*genome_length))
        end_gene = start_gene + int(parent1_portion*genome_length)
        if end_gene > genome_length:
            end_gene = genome_length

        for i in range(start_gene, end_gene):
            left.append(parent1.gene_at(i))

        for gene in parent2.get_genome():
            if gene not in left:
                right.append(gene)
        
        child_genome = left + right
        child = Individual(child_genome)

        # random mutation
        child.mutate(self.mutation_rate)
        return child

    def record_progress(self, generation, fitness):
        self.progress.append(1/fitness)
        if fitness > self.best_fitness_score:
            self.best_fitness_score = fitness
            self.best_generation = generation

    def early_stop(self, generation):
        if generation-self.best_generation > self.early_stop_rounds:
            return True
        return False


class FineTune:
    def __init__(self, gene_list) -> None:
        self.gene_list = gene_list

    def execute(self):
        pop_combined = Population()
        for i in range(5):
            print("round", i)
            ga = GA(self.gene_list, pop_size=3*len(self.gene_list), elite_size=2*len(self.gene_list), generations=40*len(self.gene_list), pop_growth=True, early_stop=100)
            pop = ga.execute().get_whole_population()
            pop_combined = pop_combined.combine(pop)

        print("final round, num members:", pop_combined.get_num_members())
        ga_final = GA(self.gene_list, pop_size=5*len(self.gene_list), elite_size=7*len(self.gene_list), generations=40*len(self.gene_list), pop_growth=True, early_stop=150)
        ga_final.population = pop_combined
        results = ga_final.execute()

        return results.fittest_genome(), results.best_fitness(), results.get_progress()