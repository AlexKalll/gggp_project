from fitness import measure_complexity

def parse_program_string(program_str):
    if not program_str:
        return []
    return program_str.split()

def calculate_complexity(program_str):
    # wrapper for measure_complexity
    return measure_complexity(program_str)

def print_population_stats(population, generation):
    # Print statistics for current population
    fitnesses = [ind.fitness for ind in population.individuals]
    
    print(f"=== Generation {generation} ===")
    print(f"Best Fitness: {max(fitnesses):.3f}")
    print(f"Average Fitness: {sum(fitnesses)/len(fitnesses):.3f}")
    print(f"Worst Fitness: {min(fitnesses):.3f}")
    print(f"Population Size: {len(population.individuals)}")
    
    # Show top 3 individuals
    print("\nTop 3 Individuals:")
    for i, ind in enumerate(population.individuals[:3]):
        print(f"  {i+1}. Fitness: {ind.fitness:.3f}, Program: {ind.phenotype}")

def save_results(best_individual, filename='gggp_results.txt'):
    """Save best results to file."""
    with open(filename, 'w') as f:
        f.write(f"Best Solution Found:\n")
        f.write(f"Fitness: {best_individual.fitness:.3f}\n")
        f.write(f"Program: {best_individual.phenotype}\n")
        f.write(f"Complexity: {calculate_complexity(best_individual.phenotype)}\n")
        f.write(f"Genotype: {best_individual.genotype}\n")
    
    print(f"Results saved to {filename}")