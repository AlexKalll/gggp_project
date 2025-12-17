
"""Population and Individual implementation for GGGP.

This file provides a single consistent Population implementation and an
Individual that supports fitness functions accepting either
`(phenotype,)` or `(phenotype, variables)`.
"""

import random
import inspect
from fitness import measure_complexity


class Individual:
    def __init__(self, genotype, grammar):
        self.genotype = genotype
        self.grammar = grammar
        self.phenotype = grammar.genotype_to_phenotype(genotype)
        self.fitness = 0.0
        self.complexity = 0

    def evaluate(self, fitness_func, variables=None):
        """Evaluate individual's fitness.

        `fitness_func` may accept either `(phenotype,)` or `(phenotype, variables)`.
        """
        try:
            sig = None
            try:
                sig = inspect.signature(fitness_func)
            except Exception:
                pass

            if sig and len(sig.parameters) >= 2:
                self.fitness = fitness_func(self.phenotype, variables)
            else:
                self.fitness = fitness_func(self.phenotype)

            self.complexity = measure_complexity(self.phenotype)
        except Exception:
            # Fall back to zero fitness on error
            self.fitness = 0.0
            self.complexity = measure_complexity(self.phenotype)

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
            [1, 0, 0, 1],  # pattern-based individuals
            [1, 2, 0],
            [0, 0, 1, 0],
            [1, 0, 2, 1],
            [2, 0],
        ]

        for pattern in patterns:
            self.individuals.append(Individual(pattern, grammar))

        for _ in range(size - len(patterns)):
            genotype = grammar.get_random_genotype(length=6)
            self.individuals.append(Individual(genotype, grammar))

        self.generation = 0
        self.best_fitness = 0.0

    def evaluate_all(self):
        for ind in self.individuals:
            ind.evaluate(self.fitness_func, variables=self.variables)

        self.individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.best_fitness = self.individuals[0].fitness
        return self.best_fitness

    def selection(self):
        """Tournament selection with elites."""
        tournament_size = 3
        selected = []

        # Keep elites
        selected.extend(self.individuals[:self.elite_size])

        # Tournament selection for the rest
        while len(selected) < self.size:
            tournament = random.sample(self.individuals, min(tournament_size, len(self.individuals)))
            winner = max(tournament, key=lambda x: x.fitness)
            selected.append(winner)

        self.individuals = selected

    def crossover(self, crossover_rate=0.8):
        """Single-point crossover."""
        new_population = self.individuals[:self.elite_size]

        while len(new_population) < self.size:
            parent1 = random.choice(self.individuals)
            parent2 = random.choice(self.individuals)

            if random.random() < crossover_rate and len(parent1.genotype) > 1 and len(parent2.genotype) > 1:
                point = random.randint(1, min(len(parent1.genotype), len(parent2.genotype)) - 1)
                child_genotype = parent1.genotype[:point] + parent2.genotype[point:]
            else:
                child_genotype = parent1.genotype.copy()

            child = Individual(child_genotype, self.grammar)
            new_population.append(child)

        self.individuals = new_population

    def mutation(self, mutation_rate=0.1):
        """Grammar-preserving mutation."""
        for i in range(self.elite_size, len(self.individuals)):
            if random.random() < mutation_rate:
                genotype = self.individuals[i].genotype.copy()
                if genotype:
                    idx = random.randint(0, len(genotype) - 1)
                    genotype[idx] = random.randint(0, 9)
                self.individuals[i] = Individual(genotype, self.grammar)

    def evolve(self, generations=50, no_improvement_limit=10):
        """Run evolution for specified generations and return best Individual."""
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
        """Get the least complex solution with fitness above threshold."""
        candidates = [ind for ind in self.individuals if ind.fitness >= threshold]

        if not candidates:
            return None

        return min(candidates, key=lambda x: x.complexity)