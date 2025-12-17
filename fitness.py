import itertools

def evaluate_program_quality(program_str, variables):
    """
    Better fitness function that rewards meaningful Boolean expressions.
    """
    if not program_str:
        return 0.0
    
    tokens = program_str.split()
    if len(tokens) == 0:
        return 0.0
    
    operators = ['AND', 'OR', 'NOT']
    
    # ===== VALIDITY CHECK =====
    # 1. Check token validity
    for token in tokens:
        if token not in variables and token not in operators:
            return 0.1  # Low score for invalid tokens
    
    # 2. Check syntax (no consecutive operators except NOT followed by variable)
    for i in range(len(tokens) - 1):
        curr, next_tok = tokens[i], tokens[i+1]
        
        # NOT can be followed by variable or NOT
        if curr == 'NOT':
            if next_tok not in variables and next_tok != 'NOT':
                return 0.2
        
        # AND/OR must be between variables or NOT expressions
        elif curr in ['AND', 'OR']:
            if next_tok in ['AND', 'OR']:
                return 0.1  # Very bad: "AND AND"
    
    # ===== SCORE CALCULATION =====
    score = 0.0
    
    # Base score for having at least one variable
    var_count = sum(1 for t in tokens if t in variables)
    if var_count >= 1:
        score += 0.3
    
    # Bonus for multiple variables
    if var_count >= 2:
        score += 0.3
    
    # Bonus for operators
    op_count = sum(1 for t in tokens if t in operators)
    if op_count >= 1:
        score += 0.2
    
    # Bonus for well-formed expressions
    # Pattern: Variable (Operator Variable)*
    if len(tokens) >= 3:
        # Check for alternating pattern
        is_well_formed = True
        for i in range(len(tokens)):
            if i % 2 == 0:  # Even positions should be variables or NOT
                if tokens[i] not in variables and tokens[i] != 'NOT':
                    is_well_formed = False
                    break
            else:  # Odd positions should be AND/OR
                if tokens[i] not in ['AND', 'OR']:
                    is_well_formed = False
                    break
        
        if is_well_formed:
            score += 0.2
    
    # Cap at 1.0
    return min(score, 1.0)

def evaluate_truth_table(program_str, variables):
    """
    Try actual Boolean evaluation for simple programs.
    """
    try:
        # For demonstration, let's use a simple target: A XOR B
        if len(variables) >= 2:
            # Test a few cases
            test_cases = [
                ({'A': False, 'B': False, 'C': False}, False),
                ({'A': False, 'B': True, 'C': False}, True),
                ({'A': True, 'B': False, 'C': False}, True),
                ({'A': True, 'B': True, 'C': False}, False),
            ]
            
            correct = 0
            for env, expected in test_cases:
                try:
                    result = evaluate_expression(program_str, env)
                    if result == expected:
                        correct += 1
                except:
                    pass
            
            return correct / len(test_cases)
        
        return evaluate_program_quality(program_str, variables)
    except:
        return evaluate_program_quality(program_str, variables)

def evaluate_expression(program_str, env):
    """Evaluate Boolean expression written in infix form using a
    shunting-yard algorithm to convert to postfix and then evaluate.
    Supports variables present in `env`, and operators `NOT`, `AND`, `OR`.
    """
    if not program_str:
        return False

    tokens = program_str.split()

    # Define operator precedence and arity
    ops = {
        'NOT': (3, 'right', 1),
        'AND': (2, 'left', 2),
        'OR': (1, 'left', 2),
    }

    # Shunting-yard: infix -> postfix
    output_queue = []
    op_stack = []

    for token in tokens:
        if token in env:
            output_queue.append(token)
        elif token in ops:
            prec, assoc, arity = ops[token]
            while op_stack:
                top = op_stack[-1]
                if top not in ops:
                    break
                top_prec, top_assoc, _ = ops[top]
                if (assoc == 'left' and prec <= top_prec) or (assoc == 'right' and prec < top_prec):
                    output_queue.append(op_stack.pop())
                else:
                    break
            op_stack.append(token)
        else:
            # Unknown token: ignore
            continue

    while op_stack:
        output_queue.append(op_stack.pop())

    # Evaluate postfix
    eval_stack = []
    for token in output_queue:
        if token in env:
            eval_stack.append(bool(env[token]))
        elif token in ops:
            _, _, arity = ops[token]
            if arity == 1:
                if not eval_stack:
                    return False
                a = eval_stack.pop()
                eval_stack.append(not a)
            else:
                if len(eval_stack) < 2:
                    return False
                b = eval_stack.pop()
                a = eval_stack.pop()
                if token == 'AND':
                    eval_stack.append(a and b)
                else:
                    eval_stack.append(a or b)
        else:
            # ignore unknown
            pass

    return eval_stack[-1] if eval_stack else False

def measure_complexity(program_str):
    """Complexity measurement."""
    if not program_str:
        return 0
    
    tokens = program_str.split()
    operators = ['AND', 'OR', 'NOT']
    op_count = sum(1 for token in tokens if token in operators)
    
    # Count unique variables
    unique_vars = len(set([t for t in tokens if t not in operators]))
    
    return op_count + (unique_vars * 0.5)

def fitness_with_penalty(program_str, variables, complexity_weight=0.02):  # Very small penalty
    """Final fitness calculation."""
    # Use truth-table accuracy as the primary fitness signal when possible.
    accuracy = evaluate_truth_table(program_str, variables)
    complexity = measure_complexity(program_str)
    fitness = accuracy - (complexity_weight * complexity)
    return max(fitness, 0.0)