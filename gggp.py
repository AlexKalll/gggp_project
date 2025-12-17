from grammar import Grammar
from population import Population
from fitness import fitness_with_penalty
from utils import print_population_stats, save_results, calculate_complexity

class GGGPSystem:
    def __init__(self, variables=None, pop_size=30, complexity_weight=0.02):
        self.variables = variables or ['A', 'B', 'C']
        self.grammar = Grammar(self.variables)
        self.fitness_func = lambda prog: fitness_with_penalty(
            prog, self.variables, complexity_weight
        )
        
        self.population = Population(
            size=pop_size,
            grammar=self.grammar,
            fitness_func=self.fitness_func,
            variables=self.variables,
            elite_size=2
        )
        
        self.best_solution = None
    
    def run_evolution(self, generations=25):
        print("=" * 60)
        print("GRAMMAR-GUIDED GENETIC PROGRAMMING SYSTEM")
        print("=" * 60)
        print(f"Variables: {self.variables}")
        print(f"Population: {self.population.size}, Generations: {generations}")
        print("=" * 60)
        
        # Initial evaluation
        self.population.evaluate_all()
        print("\nINITIAL POPULATION:")
        print_population_stats(self.population, 0)
        
        # Evolution loop
        print("\n" + "=" * 40)
        print("EVOLUTION PROGRESS")
        print("=" * 40)
        
        for gen in range(1, generations + 1):
            self.population.evolve(generations=1)  # Evolve one generation
            
            if gen % 5 == 0 or gen == 1 or gen == generations:
                print(f"\nGeneration {gen}:")
                best = self.population.individuals[0]
                print(f"  Best fitness: {best.fitness:.3f}")
                print(f"  Best program: {best.phenotype}")
                print(f"  Complexity: {calculate_complexity(best.phenotype)}")
        
        self.best_solution = self.population.individuals[0]
        
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        print(f"Total generations: {self.population.generation}")
        print(f"Best fitness: {self.best_solution.fitness:.3f}")
        print(f"Best program: {self.best_solution.phenotype}")
        print(f"Program complexity: {calculate_complexity(self.best_solution.phenotype)}")
        
        # Find least complex solution
        least_complex = self.population.get_least_complex_solution(
            threshold=self.best_solution.fitness * 0.7
        )
        
        if least_complex and least_complex.phenotype != self.best_solution.phenotype:
            print(f"\n--- Least Complex Solution (70% threshold) ---")
            print(f"Program: {least_complex.phenotype}")
            print(f"Fitness: {least_complex.fitness:.3f}")
            print(f"Complexity: {least_complex.complexity}")
        
        return self.best_solution
    
    def add_variable(self, variable):
        """Add a new variable to the system."""
        if variable not in self.variables:
            self.variables.append(variable)
            self.grammar.add_variable(variable)
            print(f"\n✓ Added variable: {variable}")
            print(f"Updated variables: {self.variables}")
    
    def test_genotype_mapping(self):
        """Test the genotype-to-phenotype mapping."""
        print("\n" + "=" * 40)
        print("GENOTYPE TO PHENOTYPE MAPPING")
        print("=" * 40)
        
        test_cases = [
            ([1, 0, 0, 1], "A AND B"),
            ([1, 2, 0], "NOT A"),
            ([0, 0, 1, 0], "A OR B"),
            ([2, 0], "A"),
        ]
        
        for genotype, expected in test_cases:
            phenotype = self.grammar.genotype_to_phenotype(genotype)
            fitness = self.fitness_func(phenotype)
            
            print(f"\nGenotype: {genotype}")
            print(f"Expected: {expected}")
            print(f"Actual:   {phenotype}")
            print(f"Fitness:  {fitness:.3f}")
            print(f"Valid:    {self.grammar.is_valid_program(phenotype)}")

def main():
    print("\n" + "=" * 60)
    print("GGGP DEMONSTRATION")
    print("=" * 60)
    
    # Initialize with 3 variables
    variables = ['A', 'B', 'C']
    
    system = GGGPSystem(
        variables=variables,
        pop_size=25,
        complexity_weight=0.02
    )
    
    # Test genotype mapping
    system.test_genotype_mapping()
    
    # Run evolution
    print("\n" + "=" * 60)
    print("STARTING EVOLUTION")
    print("=" * 60)
    
    best = system.run_evolution(generations=20)
    
    # Save results
    save_results(best)
    
    # Demonstrate adding a variable
    print("\n" + "=" * 60)
    print("DEMONSTRATING DYNAMIC VARIABLE ADDITION")
    print("=" * 60)
    system.add_variable('D')
    
    # Show it works with new variable
    test_genotype = [1, 0, 3, 2]  # Should use variable D (index 3)
    test_program = system.grammar.genotype_to_phenotype(test_genotype)
    print(f"\nTest with new variable 'D':")
    print(f"Genotype: {test_genotype}")
    print(f"Program:  {test_program}")
    print(f"Contains 'D': {'D' in test_program}")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    
    return best

if __name__ == "__main__":
    main()