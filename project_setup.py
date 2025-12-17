import os
from pathlib import Path

#  main files
files = {
    "gggp.py": "# Main GGGP implementation\n",
    "grammar.py": "# Grammar definition and parser\n",
    "population.py": "# Population management and evolution\n",
    "fitness.py": "# Fitness function with complexity penalty\n",
    "utils.py": "# Helper functions (e.g., mapping genotype to phenotype)\n",
    "README.md": "# GGGP Project\n\nGrammar-Guided Genetic Programming Implementation\n"
}

# creat tests directory
tests_dir = Path("tests")
tests_dir.mkdir(exist_ok=True)

# Test files
test_files = {
    "test_grammar.py": "# Unit tests for grammar module\n",
    "test_population.py": "# Unit tests for population module\n",
    "test_fitness.py": "# Unit tests for fitness module\n",
    "test_utils.py": "# Unit tests for utils module\n"
}

print("Creating project structure...")

# Create main files
for filename, content in files.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filename}")

# Create test files
for filename, content in test_files.items():
    filepath = tests_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: tests/{filename}")

print("Project structure created successfully!")