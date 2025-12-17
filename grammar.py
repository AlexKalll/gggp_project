import random

class Grammar:
    def __init__(self, variables=None):
        self.rules = {
            '<expr>': [
                '<term> <op_bin> <expr>',
                '<unop> <expr>',
                '<term>'
            ],
            '<op_bin>': ['AND', 'OR'],
            '<unop>': ['NOT'],
            '<term>': variables if variables else ['A', 'B', 'C']
        }
        self.start_symbol = '<expr>'
    
    def genotype_to_phenotype(self, genotype):
        """Recursive genotype-to-phenotype mapping using grammar productions.

        The genotype is consumed sequentially as a stream of decision genes. When
        the genotype runs out we wrap-around using modulo indexing so mapping is
        robust to length. This allows nested expressions such as
        (A AND (NOT B)) OR (NOT A AND B) to be constructed.
        """
        if not genotype:
            return self.rules['<term>'][0]

        # Use an index closure so recursive calls can advance the read position
        idx = 0

        def pick_gene(mod):
            nonlocal idx
            if not genotype:
                return 0
            val = genotype[idx % len(genotype)] % mod
            idx += 1
            return val

        MAX_DEPTH = 4

        def expand(symbol, depth=0):
            if symbol == '<term>':
                term_list = self.rules['<term>']
                term = term_list[pick_gene(len(term_list))]
                return term

            if symbol == '<op_bin>':
                op_list = self.rules['<op_bin>']
                return op_list[pick_gene(len(op_list))]

            if symbol == '<unop>':
                u_list = self.rules['<unop>']
                return u_list[pick_gene(len(u_list))]

            # symbol is '<expr>'
            # Prevent runaway recursion: force terminal production at max depth
            productions = self.rules['<expr>']
            if depth >= MAX_DEPTH:
                prod = '<term>'
            else:
                prod = productions[pick_gene(len(productions))]
            parts = prod.split()
            expanded = []
            for part in parts:
                if part.startswith('<') and part.endswith('>'):
                    expanded.append(expand(part, depth+1))
                else:
                    # terminals like AND/OR/NOT are returned directly
                    expanded.append(part)
            # Join with spaces; remove possible duplicate operands where possible
            return ' '.join(expanded)

        return expand(self.start_symbol)
    
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