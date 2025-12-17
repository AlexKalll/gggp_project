
import unittest
from fitness import fitness_with_penalty, measure_complexity

class TestFitness(unittest.TestCase):
    def test_measure_complexity(self):
        self.assertEqual(measure_complexity('A'), 0)
        self.assertEqual(measure_complexity('A AND B'), 1)
        self.assertEqual(measure_complexity('A AND B OR NOT C'), 3)
    
    def test_fitness_with_penalty(self):
        variables = ['A', 'B']
        fitness = fitness_with_penalty('A OR B', variables, complexity_weight=0.1)
        self.assertGreaterEqual(fitness, 0)
        self.assertLessEqual(fitness, 1)

if __name__ == '__main__':
    unittest.main()