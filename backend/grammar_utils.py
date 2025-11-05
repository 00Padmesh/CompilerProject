# grammar_utils.py

def read_grammar(grammar_text): # Changed parameter from file_path
    """
    Reads a grammar from a multi-line string.
    Each line: LHS -> RHS1 | RHS2 ...
    RHS symbols are space-separated, epsilon = eps
    """
    grammar = {}
    # Split the input string into lines
    for line in grammar_text.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        # Check for '->' to ensure it's a valid rule line
        if "->" not in line:
            continue

        lhs, rhs = line.split("->", 1) # Split only on the first '->'
        lhs = lhs.strip()
        productions = [prod.strip().split() for prod in rhs.split("|")]
        
        # If the non-terminal already exists, append rules (for grammars split on multiple lines)
        if lhs in grammar:
            grammar[lhs].extend(productions)
        else:
            grammar[lhs] = productions
            
    return grammar

# ... rest of the file


def find_symbols(grammar):
    """
    Returns sets of non-terminals and terminals.
    """
    non_terminals = set(grammar.keys())
    terminals = set()
    for rhs_list in grammar.values():
        for production in rhs_list:
            for symbol in production:
                if symbol not in non_terminals and symbol != "eps":
                    terminals.add(symbol)
    return non_terminals, terminals

# backend/grammar_utils.py

# ... (at the end of the file, after find_symbols)

def detect_direct_left_recursion(grammar):
    """
    Detects direct left recursion in a grammar.
    Returns a list of non-terminals that have direct left recursion.

    A non-terminal 'A' has direct left recursion if there is a production
    A -> A...
    """
    recursive_non_terminals = []

    for non_terminal, productions in grammar.items():
        for production in productions:
            # Check if the production is not empty and the first symbol
            # is the same as the non-terminal on the LHS
            if production and production[0] == non_terminal:
                recursive_non_terminals.append(non_terminal)
                # Once found for this non-terminal, no need to check other rules
                break

    return recursive_non_terminals

# Example usage
if __name__ == "__main__":
    grammar = read_grammar("tests/sample_grammar.txt")
    nt, t = find_symbols(grammar)
    print("Grammar:", grammar)
    print("Non-terminals:", nt)
    print("Terminals:", t)
