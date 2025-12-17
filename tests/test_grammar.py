# unit tests for grammar.py
import unittest
from grammar import Grammar

class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar(['A', 'B', 'C'])
    
    def test_initialization(self):
        self.assertEqual(self.grammar.start_symbol, '<expr>')
        self.assertIn('AND', self.grammar.rules['<op>'])
        self.assertIn('A', self.grammar.rules['<term>'])
    
    def test_add_variable(self):
        self.grammar.add_variable('D')
        self.assertIn('D', self.grammar.rules['<term>'])
    
    def test_genotype_to_phenotype(self):
        genotype = [0, 2, 2, 1, 0, 2]
        result = self.grammar.genotype_to_phenotype(genotype)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_is_valid_program(self):
        self.assertTrue(self.grammar.is_valid_program('A OR B'))
        self.assertFalse(self.grammar.is_valid_program('A FOO B'))

if __name__ == '__main__':
    unittest.main()