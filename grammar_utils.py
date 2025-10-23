# grammar_utils.py

def read_grammar(file_path):
    """
    Reads a grammar from a file.
    Each line: LHS -> RHS1 | RHS2 ...
    RHS symbols are space-separated, epsilon = ε
    """
    grammar = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            lhs, rhs = line.split("->")
            lhs = lhs.strip()
            productions = [prod.strip().split() for prod in rhs.split("|")]
            grammar[lhs] = productions
    return grammar


def find_symbols(grammar):
    """
    Returns sets of non-terminals and terminals
    """
    non_terminals = set(grammar.keys())
    terminals = set()
    for rhs_list in grammar.values():
        for production in rhs_list:
            for symbol in production:
                if symbol not in non_terminals and symbol != "ε":
                    terminals.add(symbol)
    return non_terminals, terminals


# Example usage
if __name__ == "__main__":
    grammar = read_grammar("tests/sample_grammar.txt")
    nt, t = find_symbols(grammar)
    print("Grammar:", grammar)
    print("Non-terminals:", nt)
    print("Terminals:", t)
