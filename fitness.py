import itertools

# evaluation functions for genetic programming in Boolean logic domain
def evaluate_truth_table(program_str, variables):    
    if not program_str:
        return 0.0
    
    def target_function(*args):
        return sum(args) == 1
    
    correct = 0
    total = 0
    

    for combination in itertools.product([0, 1], repeat=len(variables)):
        env = {var: bool(val) for var, val in zip(variables, combination)}
        
        tokens = program_str.split()
        result = evaluate_tokens(tokens, env)
        
        # Compare with target
        target_result = target_function(*combination)
        if result == target_result:
            correct += 1
        total += 1

    
    return correct / total if total > 0 else 0.0

# Simple evaluator for bool expressions
def evaluate_tokens(tokens, env):
    if len(tokens) == 1:
        return env.get(tokens[0], False)
    
    if tokens[0] == 'NOT':
        return not evaluate_tokens(tokens[1:], env)
    
    # Handle binary operators
    for i, token in enumerate(tokens):
        if token in ['AND', 'OR']:
            left = evaluate_tokens(tokens[:i], env)
            right = evaluate_tokens(tokens[i+1:], env)
            
            if token == 'AND':
                return left and right
            else:  # or
                return left or right
    
    return False

def measure_complexity(program_str):
    if not program_str:
        return 0

    tokens = program_str.split()
    operators = ['AND', 'OR', 'NOT']
    op_count = sum(1 for token in tokens if token in operators)
    return op_count

# Calculate fitness with complexity penalty, higher is better
def fitness_with_penalty(program_str, variables, complexity_weight=0.1):
    accuracy = evaluate_truth_table(program_str, variables)
    
    complexity = measure_complexity(program_str)    
    fitness = accuracy - (complexity_weight * complexity / 10.0)
    
    return max(fitness, 0.0)