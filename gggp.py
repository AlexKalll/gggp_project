from grammar import Grammar
from population import Population
from fitness import fitness_with_penalty
from utils import print_population_stats, save_results, calculate_complexity

class GGGPSystem:
    def __init__(self, variables=None, pop_size=100, complexity_weight=0.1):
        self.variables = variables or ['A', 'B', 'C']
        
        # Initialize grammar with variables (use simple decoder for predictable mapping)
        self.grammar = Grammar(self.variables, simple=True)
        
        # Initialize fitness function with complexity penalty
        # Accept (prog, variables) signature used by Population/Individual
        self.fitness_func = lambda prog, vars=None: fitness_with_penalty(prog, self.variables, complexity_weight)
        
        # Initialize population
        self.population = Population(
            size=pop_size,
            grammar=self.grammar,
            fitness_func=self.fitness_func,
            variables=self.variables,
            elite_size=1
        )
        
        self.best_solution = None
    
    def run_evolution(self, generations=100):
        print("=" * 50)
        print("Starting Grammar-Guided Genetic Programming")
        print(f"Variables: {self.variables}")
        print(f"Population size: {self.population.size}")
        print(f"Max generations: {generations}")
        print("=" * 50)
        
        # Initial evaluation
        self.population.evaluate_all()
        print_population_stats(self.population, 0)
        
        # Run evolution
        self.best_solution = self.population.evolve(generations=generations)
        
        # Final results
        print("\n" + "=" * 50)
        print("EVOLUTION COMPLETE")
        print("=" * 50)
        print(f"Generations run: {self.population.generation}")
        print(f"Best fitness: {self.best_solution.fitness:.3f}")
        print(f"Best program: {self.best_solution.phenotype}")
        print(f"Program complexity: {calculate_complexity(self.best_solution.phenotype)}")
        
        # Get least complex solution
        least_complex = self.population.get_least_complex_solution(threshold=self.best_solution.fitness * 0.9)
        
        if least_complex:
            print(f"\nLeast complex solution (within 90% of best):")
            print(f"  Program: {least_complex.phenotype}")
            print(f"  Fitness: {least_complex.fitness:.3f}")
            print(f"  Complexity: {calculate_complexity(least_complex.phenotype)}")
        
        return self.best_solution
    
    def add_variable(self, variable):
        self.grammar.add_variable(variable)
        if variable not in self.variables:
            self.variables.append(variable)
        print(f"Added variable: {variable}")
    
    def test_genotype_mapping(self, genotype=None):
        genotype = genotype or [0, 2, 2, 1, 0, 2] 
        phenotype = self.grammar.genotype_to_phenotype(genotype)
        
        print(f"\nGenotype-to-Phenotype Test:")
        print(f"Genotype: {genotype}")
        print(f"Phenotype: {phenotype}")
        print(f"Is valid: {self.grammar.is_valid_program(phenotype)}")
        
        return phenotype

def main():
    variables = ['A', 'B', 'C', 'D']  #any number of variables
    
    # Initialize system
    system = GGGPSystem(
        variables=variables,
        pop_size=100,
        complexity_weight=0.02
    )
    
    system.test_genotype_mapping([0, 2, 2, 1, 0, 2])

    best = system.run_evolution(generations=100)
    save_results(best)
    
    return best

if __name__ == "__main__":
    main()