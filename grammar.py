import random

class Grammar:
    def __init__(self, variables=None, simple=True):
        # allow a simple positional decoder (matches earlier examples)
        self.simple = simple
        #  grammar rules for boolean expressions (used in complex mode)
        self.rules = {
            '<expr>': [
                '<expr> <op_bin> <expr>',
                '<unop> <expr>',
                '<term>'
            ],
            '<op_bin>': ['AND', 'OR'],
            '<unop>': ['NOT'],
            '<term>': variables if variables else ['A', 'B', 'C']
        }

        self.rule_counts = {}
        for nt, productions in self.rules.items():
            self.rule_counts[nt] = len(productions)

        # Backwards compatibility: keep '<op>' as combined unary+binary operators
        combined_ops = []
        if '<op_bin>' in self.rules:
            combined_ops.extend(self.rules['<op_bin>'])
        if '<unop>' in self.rules:
            combined_ops.extend(self.rules['<unop>'])
        # ensure '<op>' exists for older callers/tests
        self.rules['<op>'] = combined_ops
        self.rule_counts['<op>'] = len(combined_ops)

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
        # Simple positional decoder (keeps tests / examples stable)
        if self.simple:
            if not genotype:
                return 'A'

            expr_type = genotype[0] % 3
            # <term> <op> <term>
            if expr_type == 0:
                if len(genotype) < 4:
                    return 'A AND B'
                term1 = self.rules['<term>'][genotype[1] % len(self.rules['<term>'])]
                # choose only a binary operator here
                op = self.rules['<op_bin>'][genotype[2] % len(self.rules['<op_bin>'])]
                term2 = self.rules['<term>'][genotype[3] % len(self.rules['<term>'])]

                # avoid trivial duplicates when possible
                if term1 == term2 and len(self.rules['<term>']) > 1:
                    term2 = self.rules['<term>'][(genotype[3] + 1) % len(self.rules['<term>'])]

                return f"{term1} {op} {term2}"

            # <op> <term> (unary) or binary using same pattern
            if expr_type == 1:
                if len(genotype) < 3:
                    return 'NOT A'
                op = self.rules['<unop>'][genotype[1] % len(self.rules['<unop>'])]
                term = self.rules['<term>'][genotype[2] % len(self.rules['<term>'])]
                if op == 'NOT':
                    return f"{op} {term}"
                else:
                    term2 = self.rules['<term>'][genotype[3] % len(self.rules['<term>'])] if len(genotype) > 3 else term
                    if term == term2 and len(self.rules['<term>']) > 1:
                        term2 = self.rules['<term>'][(genotype[3] + 1) % len(self.rules['<term>'])]
                    return f"{term} {op} {term2}"

            # Just a term
            return self.rules['<term>'][genotype[1] % len(self.rules['<term>'])] if len(genotype) > 1 else self.rules['<term>'][0]

        # Complex grammar-driven decoder (existing implementation)
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
            if not tokens:
                return False

            terms = set(self.rules['<term>'])
            bin_ops = set(self.rules.get('<op_bin>', ['AND', 'OR']))
            un_ops = set(self.rules.get('<unop>', ['NOT']))

            i = 0
            # allow sequences with optional leading NOTs
            def parse_factor(idx):
                # handle repeated NOTs
                while idx < len(tokens) and tokens[idx] in un_ops:
                    idx += 1
                if idx < len(tokens) and tokens[idx] in terms:
                    return idx + 1
                return -1

            # first factor
            idx = parse_factor(0)
            if idx == -1:
                return False

            # then zero or more (bin_op factor)
            while idx < len(tokens):
                if tokens[idx] not in bin_ops:
                    return False
                idx += 1
                idx2 = parse_factor(idx)
                if idx2 == -1:
                    return False
                idx = idx2

            return True
        except Exception:
            return False
    
    def get_random_genotype(self, length=10):
        rand_genotype = []
        for _ in range(length):
            curr = random.randint(0, 9)
            rand_genotype.append(curr)

        return rand_genotype