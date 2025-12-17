
from fitness import measure_complexity

import random

class Individual:    
    def __init__(self, genotype, grammar):
        self.genotype = genotype
        self.grammar = grammar
        self.phenotype = grammar.genotype_to_phenotype(genotype)
        self.fitness = 0.0
        self.complexity = 0
    
    def evaluate(self, fitness_func, variables):
        """Evaluate individual's fitness."""
        try:
            self.fitness = fitness_func(self.phenotype, variables)
        except Exception:
            pass 
        return self.fitness
    
    def __repr__(self):
        return f"Individual(fitness={self.fitness:.3f}, program='{self.phenotype}')"

# Manages population of individuals and evolution process.
class Population:    
    def __init__(self, size, grammar, fitness_func, variables, elite_size=2):
        """Initialize population.
            size: Population size
            grammar: Grammar instance
            fitness_func: Fitness function
            variables: List of variables
            elite_size: Number of elite individuals to preserve
        """
        self.size = size
        self.grammar = grammar
        self.fitness_func = fitness_func
        self.variables = variables
        self.elite_size = elite_size
        
        # Initialize population with useful seed patterns then random individuals
        self.individuals = []
        seed_patterns = [
            [1, 0, 0, 1],  # A AND B
            [0, 0, 1, 0],  # A OR B
            [1, 2, 0],     # NOT A
            [1, 0, 2, 1],  # A AND C
        ]

        for pat in seed_patterns:
            if len(self.individuals) < size:
                self.individuals.append(Individual(pat, grammar))

        # Fill rest randomly
        for _ in range(size - len(self.individuals)):
            genotype = grammar.get_random_genotype(length=15)
            self.individuals.append(Individual(genotype, grammar))
        
        self.generation = 0
        self.best_fitness = 0.0
    
    def evaluate_all(self):
        """Evaluate fitness for all individuals."""
        for ind in self.individuals:
            ind.evaluate(self.fitness_func, self.variables)
        
        # Sort by fitness (descending)
        self.individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.best_fitness = self.individuals[0].fitness
        
        return self.best_fitness
    
    def selection(self):
        """Tournament selection."""
        tournament_size = 3
        selected = []
        
        # Keep elites
        selected.extend(self.individuals[:self.elite_size])
        
        # Tournament selection for rest
        while len(selected) < self.size:
            tournament = random.sample(self.individuals, tournament_size)
            winner = max(tournament, key=lambda x: x.fitness)
            selected.append(winner)
        
        self.individuals = selected
    
    def crossover(self, crossover_rate=0.8):
        """Grammar-preserving crossover."""
        new_population = self.individuals[:self.elite_size]
        
        while len(new_population) < self.size:
            parent1 = random.choice(self.individuals)
            parent2 = random.choice(self.individuals)
            
            if random.random() < crossover_rate and len(parent1.genotype) > 2:
                # Single-point crossover
                point = random.randint(1, len(parent1.genotype) - 1)
                child_genotype = parent1.genotype[:point] + parent2.genotype[point:]
            else:
                # No crossover, copy parent
                child_genotype = parent1.genotype.copy()
            
            child = Individual(child_genotype, self.grammar)
            new_population.append(child)
        
        self.individuals = new_population
    
    def mutation(self, mutation_rate=0.1):
        """Grammar-preserving mutation."""
        for i in range(self.elite_size, len(self.individuals)):
            if random.random() < mutation_rate:
                genotype = self.individuals[i].genotype.copy()

                # Mutate: change or insert a gene with reasonable probability
                if genotype and random.random() < 0.8:
                    idx = random.randint(0, len(genotype) - 1)
                    genotype[idx] = random.randint(0, 9)
                else:
                    genotype.append(random.randint(0, 9))

                # Update individual
                self.individuals[i] = Individual(genotype, self.grammar)
    
    def evolve(self, generations=50, no_improvement_limit=None):
        """
        Run evolution for specified generations. returns Individual: Best solution found
        """
        best_history = []
        no_improvement = 0
        
        for gen in range(generations):
            self.evaluate_all()
            best = self.individuals[0]
            best_history.append(best.fitness)
            
            # Check for convergence
            if len(best_history) > 1:
                if best_history[-1] <= best_history[-2]:
                    no_improvement += 1
                else:
                    no_improvement = 0
            
            if no_improvement_limit is not None and no_improvement >= no_improvement_limit:
                print(f"Stopping early at generation {gen} (no improvement)")
                break
            
            # Evolutionary operators
            self.selection()
            self.crossover()
            # slightly higher mutation to improve exploration
            self.mutation(mutation_rate=0.2)
            
            self.generation += 1
        
        # Final evaluation
        self.evaluate_all()
        return self.individuals[0]
    
    def get_least_complex_solution(self, threshold=0.9):
        """
        Get the least complex solution with fitness above threshold. returns Individual or None
        """
        # Filter individuals above threshold
        candidates = [ind for ind in self.individuals 
                     if ind.fitness >= threshold]
        
        if not candidates:
            return None
        
        # Select least complex
        return min(candidates, key=lambda x: measure_complexity(x.phenotype))