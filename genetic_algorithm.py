from collections import namedtuple
import random
import snake_ai

POPULATION_SIZE = 50
MAX_GENERATIONS = 100
DIRECTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
MUTATION_RATE = 0.1

# Initializes the first generation with a set of random directions.
def initPop():
    return [[random.choice(DIRECTIONS) for _ in range(50)] for _ in range(POPULATION_SIZE)]

# Fitness score determined by snakes score in game.
def fitness(individual):
    fitness = snake_ai.main(individual)
    return fitness

# Random sample of 10 are chosen from the population (not used in the code currently)
def tournament_selection(population):
    selected = []
    for _ in population:
        random.choice
        selected.append( (random.sample(population, 10)) )
    return selected

# Parents are crossed over to make a child for the next generation
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1))
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# Mutation introduced to population
def mutate(individual):
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = random.choice(DIRECTIONS)   # The directions made by the snake are mutated
    return individual

def algorithm():
    max_score = 0
    population = initPop()

    for generation in range(MAX_GENERATIONS):
        individual = []
        for s in population:
            score, moves = snake_ai.main(s) 
            if score > max_score:
                max_score = score
            individual.append( (score, moves) ) # Score and moves made by snake are recorded

        # Individuals are sorted by scores
        individual = sorted(individual, key=lambda x: x[0])
        individual.reverse()

        selected_parents = individual[:5]   # Top 5 parents are selected for crossover
        scores =[item[0] for item in individual]
        parents = [item[1] for item in selected_parents]

        offspring = []
        for _ in range(POPULATION_SIZE):    # Parents in top 5 are randomly selected to crossover until population size is reached
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1,parent2)
            offspring.append(child)

        mutated_offspring = [mutate(individual) for individual in offspring]    # Some of the offspring are mutated (the directions made in game are mutated)

        population = mutated_offspring  # Reintroduce new population with offspring

        print(f"=== Generation {generation} ===")
        print(f'Scores: {scores}')
        print(f"Best score = {scores[0]}\n")
        print(f'Max Score = {max_score}')

    return max_score    # Max score out of all generations is returned
