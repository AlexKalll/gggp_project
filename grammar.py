import random

class Grammar:
    def __init__(self, variables=None):
        self.rules = {
            '<expr>': [
                '<term> <op> <term>',
                '<op> <term>',
                '<term>'
            ],
            '<op>': ['AND', 'OR', 'NOT'],
            '<term>': variables if variables else ['A', 'B', 'C']
        }
        self.start_symbol = '<expr>'
    
    def genotype_to_phenotype(self, genotype):
        """Simpler and more reliable mapping."""
        # Use first gene to choose expression type
        if not genotype:
            return "A"
        
        expr_type = genotype[0] % 3
        
        if expr_type == 0:  # <term> <op> <term>
            if len(genotype) < 3:
                return "A AND B"
            term1_idx = genotype[1] % len(self.rules['<term>'])
            op_idx = genotype[2] % len(self.rules['<op>'])
            term2_idx = genotype[3] % len(self.rules['<term>']) if len(genotype) > 3 else 0
            
            term1 = self.rules['<term>'][term1_idx]
            op = self.rules['<op>'][op_idx]
            term2 = self.rules['<term>'][term2_idx]
            
            return f"{term1} {op} {term2}"
            
        elif expr_type == 1:  # <op> <term>
            if len(genotype) < 2:
                return "NOT A"
            op_idx = genotype[1] % len(self.rules['<op>'])
            term_idx = genotype[2] % len(self.rules['<term>']) if len(genotype) > 2 else 0
            
            op = self.rules['<op>'][op_idx]
            term = self.rules['<term>'][term_idx]
            
            # NOT is the only unary operator
            if op == 'NOT':
                return f"{op} {term}"
            else:
                # For AND/OR, need two terms
                term2_idx = genotype[3] % len(self.rules['<term>']) if len(genotype) > 3 else 1
                term2 = self.rules['<term>'][term2_idx]
                return f"{term} {op} {term2}"
                
        else:  # Just <term>
            term_idx = genotype[1] % len(self.rules['<term>']) if len(genotype) > 1 else 0
            return self.rules['<term>'][term_idx]
    
    def is_valid_program(self, program_str):
        """Check if program is valid Boolean expression."""
        tokens = program_str.split()
        if not tokens:
            return False
        
        operators = ['AND', 'OR', 'NOT']
        variables = self.rules['<term>']
        
        # Quick check: all tokens must be valid
        for token in tokens:
            if token not in variables and token not in operators:
                return False
        
        return True
    
    def get_random_genotype(self, length=10):
        return [random.randint(0, 9) for _ in range(length)]
    
    def add_variable(self, variable):
        if variable not in self.rules['<term>']:
            self.rules['<term>'].append(variable)
    
    def set_variables(self, variables):
        self.rules['<term>'] = variables