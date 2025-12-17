import unittest
from grammar import Grammar
from population import Individual, Population
from fitness import fitness_with_penalty

class TestPopulation(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar(['A', 'B'])
        # fitness_func must accept (prog, variables)
        self.fitness_func = lambda prog, vars: fitness_with_penalty(prog, vars)
        self.variables = ['A', 'B']
    
    def test_individual_creation(self):
        genotype = [1, 2, 3, 4, 5]
        ind = Individual(genotype, self.grammar)
        self.assertEqual(ind.genotype, genotype)
        self.assertIsInstance(ind.phenotype, str)
    
    def test_population_initialization(self):
        pop = Population(10, self.grammar, self.fitness_func, ['A', 'B'])
        self.assertEqual(len(pop.individuals), 10)
    
    def test_evaluation(self):
        pop = Population(5, self.grammar, self.fitness_func, ['A', 'B'])
        best = pop.evaluate_all()
        self.assertIsInstance(best, float)

if __name__ == '__main__':
    unittest.main()