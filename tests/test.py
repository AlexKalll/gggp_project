# test_quick.py
from grammar import Grammar

grammar = Grammar(['A', 'B', 'C'])
test_genotype = [0, 2, 2, 1, 0, 2, 0, 1, 2, 0, 1, 2]  # Longer genotype
program = grammar.genotype_to_phenotype(test_genotype)
print(f"Genotype: {test_genotype}")
print(f"Program: {program}")
print(f"Is valid: {grammar.is_valid_program(program)}")

# Test fitness
from fitness import fitness_with_penalty
fitness = fitness_with_penalty(program, ['A', 'B', 'C'])
print(f"Fitness: {fitness:.3f}")