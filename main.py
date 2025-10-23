from grammar_utils import read_grammar, find_symbols
from first_follow import compute_first, compute_follow


def compute_parsing_table(grammar, first, follow):
    """Build the LL(1) parsing table with explicit conflict reporting."""
    table = {nt: {} for nt in grammar}
    conflicts = []

    for A in grammar:
        for production in grammar[A]:
            # Compute FIRST of this production
            first_alpha = set()
            for sym in production:
                if sym in grammar:  # non-terminal
                    first_alpha |= (first[sym] - {'ε'})
                    if 'ε' not in first[sym]:
                        break
                else:  # terminal
                    first_alpha.add(sym)
                    break
            else:
                first_alpha.add('ε')

            # Fill table for each terminal in FIRST(alpha)
            for terminal in first_alpha - {'ε'}:
                if terminal in table[A]:
                    conflicts.append((A, terminal, table[A][terminal], production, "FIRST/FIRST"))
                table[A][terminal] = production

            # If epsilon is in FIRST(alpha), add entries for FOLLOW(A)
            if 'ε' in first_alpha:
                for terminal in follow[A]:
                    if terminal in table[A]:
                        conflicts.append((A, terminal, table[A][terminal], production, "FIRST/FOLLOW"))
                    table[A][terminal] = production

    # Print all conflicts explicitly
    if conflicts:
        print("\n=== Conflicts Detected ===")
        for A, terminal, existing_prod, new_prod, conflict_type in conflicts:
            print(f"{conflict_type} conflict for {A} on '{terminal}':")
            print(f"    Existing: {A} -> {' '.join(existing_prod)}")
            print(f"    New     : {A} -> {' '.join(new_prod)}")
        print("==========================\n")

    return table


def print_table(table):
    """Nicely print the LL(1) parsing table."""
    print("\n=== LL(1) Parsing Table ===")
    for nt, entries in table.items():
        for term, prod in entries.items():
            rhs = " ".join(prod)
            print(f"M[{nt}, {term}] = {nt} -> {rhs}")
    print("===========================\n")


def main():
    print("Interactive LL(1) Grammar Validator and Parser Visualizer — Phase 1\n")

    # 1. Read grammar file
    file_path = "tests/sample_grammars.txt"
    grammar = read_grammar(file_path)
    print("Grammar loaded successfully!\n")

    # 2. Identify symbols
    non_terminals, terminals = find_symbols(grammar)
    print(f"Non-terminals: {non_terminals}")
    print(f"Terminals: {terminals}\n")

    # 3. Compute FIRST sets
    first = compute_first(grammar)
    print("FIRST sets:")
    for nt, s in first.items():
        print(f"FIRST({nt}) = {s}")
    print()

    # 4. Compute FOLLOW sets
    start_symbol = list(grammar.keys())[0]  # assume first rule is start symbol
    follow = compute_follow(grammar, first, start_symbol)
    print("FOLLOW sets:")
    for nt, s in follow.items():
        print(f"FOLLOW({nt}) = {s}")
    print()

    # 5. Build LL(1) parsing table
    table = compute_parsing_table(grammar, first, follow)

    # 6. Display parsing table
    print_table(table)

    # 7. LL(1) validation summary
    print("LL(1) Validation Completed.\n")
    if all(not table[nt].get(term) for nt in table for term in table[nt]):
        print("No conflicts detected. Your grammar is LL(1)-compatible.")
    else:
        print("Conflicts were detected. See above for details.")


if __name__ == "__main__":
    main()
