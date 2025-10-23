def read_grammar(file_path):
    grammar = {}
    with open(file_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            lhs, rhs = line.strip().split('->')
            lhs = lhs.strip()
            productions = [p.strip().split() for p in rhs.split('|')]
            grammar[lhs] = productions
    return grammar


def find_symbols(grammar):
    non_terminals = set(grammar.keys())
    terminals = set()
    for rhs_list in grammar.values():
        for rule in rhs_list:
            for symbol in rule:
                if symbol not in non_terminals and symbol != 'ε':
                    terminals.add(symbol)
    return non_terminals, terminals



if __name__ == "__main__":
    g = read_grammar("tests/sample_grammars.txt")
    print(g)
    nt, t = find_symbols(g)
    print("Non-terminals:", nt)
    print("Terminals:", t)
