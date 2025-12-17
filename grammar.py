import random

class Grammar:    
    def __init__(self, variables=None):
        #  grammar rules for boolean expressions
        self.rules = {
            '<expr>': [
                '<expr> <op> <expr>',
                '<op> <expr>',
                '<term>'
            ],
            '<op>': ['AND', 'OR', 'NOT'],
            '<term>': variables if variables else ['A', 'B', 'C']
        }
        
        self.rule_counts = {}
        for nt, productions in self.rules.items():
            self.rule_counts[nt] = len(productions)

        self.start_symbol = '<expr>'
    
    # Add a new terminal variable to the grammar
    def add_variable(self, variable):
        if variable not in self.rules['<term>']:
            self.rules['<term>'].append(variable)
            self.rule_counts['<term>'] = len(self.rules['<term>'])
    
    # Set the terminal variables dynamically
    def set_variables(self, variables):
        self.rules['<term>'] = variables
        self.rule_counts['<term>'] = len(variables)
    
    # Convert genotype to phenotype (program string)
    def genotype_to_phenotype(self, genotype):
        stack = [self.start_symbol]
        output = []
        gene_index = 0
        
        # Map genotype through production rules
        while stack and gene_index < len(genotype):
            current = stack.pop(0)
            
            if current in self.rules:
                productions = self.rules[current]
                choice = genotype[gene_index] % len(productions)
                gene_index += 1
                
                # Expand non-terminal
                production = productions[choice]
                symbols = production.split()

                stack = symbols + stack
            else:
                output.append(current)
        
        while stack:
            symbol = stack.pop(0)
            if symbol not in ['<expr>', '<op>', '<term>']:
                output.append(symbol)
        
        return ' '.join(output).replace('<', '').replace('>', '').strip()
    
    # Check if program string follows grammar rules
    def is_valid_program(self, program_str):
        try:
            tokens = program_str.split()
            valid_terms = set(self.rules['<term>'])
            valid_ops = set(self.rules['<op>'])
            
            for token in tokens:
                if token not in valid_terms and token not in valid_ops:
                    return False
            return True
        except:
            return False
    
    def get_random_genotype(self, length=10):
        rand_genotype = []
        for _ in range(length):
            curr = random.randint(0, 9)
            rand_genotype.append(curr)

        return rand_genotype