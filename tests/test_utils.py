
import unittest
from utils import calculate_complexity, parse_program_string

class TestUtils(unittest.TestCase):
    def test_calculate_complexity(self):
        self.assertEqual(calculate_complexity('A AND B'), 1)
    
    def test_parse_program_string(self):
        result = parse_program_string('A OR B')
        self.assertEqual(result, ['A', 'OR', 'B'])

if __name__ == '__main__':
    unittest.main()