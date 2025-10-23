# parsing_table.py

def compute_parsing_table(grammar, first, follow):
    """
    Build the LL(1) parsing table.
    Returns:
        table: dict of table[NonTerminal][Terminal] = production
        conflicts: list of conflicts (empty if grammar is LL(1))
    """
    table = {nt: {} for nt in grammar}
    conflicts = []

    for A in grammar:
        for production in grammar[A]:
            # Compute FIRST(alpha) for the production
            first_alpha = set()
            for sym in production:
                if sym in grammar:  # non-terminal
                    first_alpha |= (first[sym] - {'eps'})
                    if 'eps' not in first[sym]:
                        break
                else:  # terminal
                    first_alpha.add(sym)
                    break
            else:
                first_alpha.add('eps')

            # Fill table for terminals in FIRST(alpha)
            for terminal in first_alpha - {'eps'}:
                if terminal in table[A]:
                    conflicts.append((A, terminal, table[A][terminal], production, "FIRST/FIRST"))
                table[A][terminal] = production

            # If epsilon is in FIRST(alpha), add entries for FOLLOW(A)
            if 'eps' in first_alpha:
                for terminal in follow[A]:
                    if terminal in table[A]:
                        conflicts.append((A, terminal, table[A][terminal], production, "FIRST/FOLLOW"))
                    table[A][terminal] = production

    return table, conflicts


def print_parsing_table(table):
    """Nicely print the LL(1) parsing table"""
    print("\n=== LL(1) Parsing Table ===")
    for nt, entries in table.items():
        for term, prod in entries.items():
            rhs = " ".join(prod)
            print(f"M[{nt}, {term}] = {nt} -> {rhs}")
    print("===========================\n")


def print_conflicts(conflicts):
    """Print detected conflicts clearly"""
    if conflicts:
        print("\n=== Conflicts Detected ===")
        for A, terminal, existing_prod, new_prod, conflict_type in conflicts:
            print(f"{conflict_type} conflict for {A} on '{terminal}':")
            print(f"    Existing: {A} -> {' '.join(existing_prod)}")
            print(f"    New     : {A} -> {' '.join(new_prod)}")
        print("==========================\n")
    else:
        print("No conflicts detected. Grammar is LL(1)-compatible.\n")


# Example usage
if __name__ == "__main__":
    from grammar_utils import read_grammar
    from first_follow import compute_first, compute_follow

    grammar = read_grammar("tests/sample_grammar.txt")
    start_symbol = list(grammar.keys())[0]

    first = compute_first(grammar)
    follow = compute_follow(grammar, first, start_symbol)

    table, conflicts = compute_parsing_table(grammar, first, follow)
    print_parsing_table(table)
    print_conflicts(conflicts)