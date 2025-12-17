
from fitness import measure_complexity
import random

class Individual:
    def __init__(self, genotype, grammar):
        self.genotype = genotype
        self.grammar = grammar
        self.phenotype = grammar.genotype_to_phenotype(genotype)
        self.fitness = 0.0
        self.complexity = 0
    
    def evaluate(self, fitness_func):
        """Evaluate individual's fitness - fitness_func takes only phenotype."""
        try:
            self.fitness = fitness_func(self.phenotype)
            self.complexity = measure_complexity(self.phenotype)
        except Exception:
            self.fitness = 0.0
        return self.fitness
    
    def __repr__(self):
        return f"Ind(f={self.fitness:.3f}, p='{self.phenotype}')"

class Population:
    def __init__(self, size, grammar, fitness_func, variables, elite_size=2):
        self.size = size
        self.grammar = grammar
        self.fitness_func = fitness_func
        self.variables = variables
        self.elite_size = elite_size
        
        # Create diverse initial population
        self.individuals = []
        patterns = [
            [1, 0, 0, 1],  # A AND B
            [1, 2, 0],     # NOT A
            [0, 0, 1, 0],  # A OR B
            [1, 0, 2, 1],  # A AND C
            [2, 0],        # Just A
        ]
        
        # Add some pattern-based individuals
        for pattern in patterns:
            self.individuals.append(Individual(pattern, grammar))
        
        # Add random individuals
        for _ in range(size - len(patterns)):
            genotype = grammar.get_random_genotype(length=6)
            self.individuals.append(Individual(genotype, grammar))
        
        self.generation = 0
        self.best_fitness = 0.0
    
    def evaluate_all(self):
        for ind in self.individuals:
            ind.evaluate(self.fitness_func)
        
        self.individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.best_fitness = self.individuals[0].fitness
        return self.best_fitness
    
    def selection(self):
        """Roulette wheel selection for more diversity."""
        # Keep elites
        selected = self.individuals[:self.elite_size]
        
        # Calculate total fitness for roulette wheel
        total_fitness = sum(max(ind.fitness, 0.01) for ind in self.individuals)
        
        # Select rest using roulette wheel
        while len(selected) < self.size:
            spin = random.random() * total_fitness
            cumulative = 0
            
            for ind in self.individuals:
                cumulative += max(ind.fitness, 0.01)
                if cumulative >= spin:
                    selected.append(ind)
                    break
        
        self.individuals = selected
    
    def crossover(self, crossover_rate=0.7):
        new_population = self.individuals[:self.elite_size]
        
        while len(new_population) < self.size:
            parent1 = random.choice(self.individuals)
            parent2 = random.choice(self.individuals)
            
            if random.random() < crossover_rate:
                # Uniform crossover
                child_genotype = []
                for i in range(min(len(parent1.genotype), len(parent2.genotype))):
                    if random.random() < 0.5:
                        child_genotype.append(parent1.genotype[i])
                    else:
                        child_genotype.append(parent2.genotype[i])
                
                # If genotypes different lengths, extend
                if len(parent1.genotype) > len(child_genotype):
                    child_genotype.extend(parent1.genotype[len(child_genotype):])
                elif len(parent2.genotype) > len(child_genotype):
                    child_genotype.extend(parent2.genotype[len(child_genotype):])
            else:
                child_genotype = parent1.genotype.copy()
            
            child = Individual(child_genotype, self.grammar)
            new_population.append(child)
        
        self.individuals = new_population
    
    def mutation(self, mutation_rate=0.2):  # Higher mutation
        for i in range(self.elite_size, len(self.individuals)):
            if random.random() < mutation_rate:
                genotype = self.individuals[i].genotype.copy()
                
                # Mutate: change, add, or remove a gene
                mutation_type = random.random()
                
                if mutation_type < 0.7 and genotype:  # Change a gene
                    idx = random.randint(0, len(genotype) - 1)
                    genotype[idx] = random.randint(0, 9)
                
                elif mutation_type < 0.85:  # Add a gene
                    genotype.append(random.randint(0, 9))
                
                elif len(genotype) > 1:  # Remove a gene
                    idx = random.randint(0, len(genotype) - 1)
                    genotype.pop(idx)
                
                self.individuals[i] = Individual(genotype, self.grammar)
    
    def evolve(self, generations=30):
        best_history = []
        
        for gen in range(generations):
            self.evaluate_all()
            best_history.append(self.best_fitness)
            
            if gen > 10 and best_history[-1] <= max(best_history[:-5]):
                # Increase mutation if stagnating
                self.mutation(mutation_rate=0.3)
            else:
                self.mutation(mutation_rate=0.2)
            
            self.selection()
            self.crossover()
            
            self.generation += 1
        
        self.evaluate_all()
        return self.individuals[0]
    
    def get_least_complex_solution(self, threshold=0.5):
        candidates = [ind for ind in self.individuals if ind.fitness >= threshold]
        if not candidates:
            candidates = self.individuals[:3]  # Fallback to top 3
        
        return min(candidates, key=lambda x: x.complexity)
    
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
                genotype = self.individuals[i].genotype
                
                # Mutate random gene
                idx = random.randint(0, len(genotype) - 1)
                genotype[idx] = random.randint(0, 9)
                
                # Update individual
                self.individuals[i] = Individual(genotype, self.grammar)
    
    def evolve(self, generations=50, no_improvement_limit=10):
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
            
            if no_improvement >= no_improvement_limit:
                print(f"Stopping early at generation {gen} (no improvement)")
                break
            
            # Evolutionary operators
            self.selection()
            self.crossover()
            self.mutation()
            
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