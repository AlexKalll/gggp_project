# Grammar-Guided Genetic Programming (GGGP) System

A Python implementation of Grammar-Guided Genetic Programming with complexity penalty and dynamic variable support.

## Features

- **Generic grammar** that accepts any number of variables
- **Complexity penalty** in fitness function
- **Least complex solution** selection
- **Grammar-preserving** crossover and mutation
- **Unit tests** for all main components
- **Modular design** for easy extension

## Project Structure

```
gggp_project/
├── gggp.py              # Main system
├── grammar.py           # Grammar definition
├── population.py        # Population management
├── fitness.py           # Fitness with penalty
├── utils.py             # Helper functions
├── tests/               # Unit tests
├── venv/               # environment folder
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Installation

```bash
# Clone repository
git clone https://github.com/AlexKalll/gggp_project.git
cd gggp_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
#  or  # for Windows
python -m venv venv
source venv/Scripts/activate
# Install requirements

pip install -r requirements.txt
```

## Usage

```python
from gggp import GGGPSystem

# Initialize with variables
variables = ['A', 'B', 'C', 'D']
system = GGGPSystem(variables=variables)

# Run evolution
best_solution = system.run_evolution(generations=50)

print(f"Best program: {best_solution.phenotype}")
print(f"Fitness: {best_solution.fitness}")
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_grammar.py
```

## Key Features

1. **Grammar-guided operations**: All crossover and mutation respect grammar rules
2. **Complexity penalty**: Fitness includes penalty for program complexity
3. **Least complex selection**: Can retrieve simplest solution within fitness threshold
4. **Dynamic variables**: Grammar can be extended with new variables at runtime
