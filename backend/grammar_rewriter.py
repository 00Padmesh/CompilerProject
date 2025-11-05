# backend/grammar_rewriter.py

def eliminate_direct_left_recursion(grammar):
    """
    Rewrites a grammar to eliminate direct left recursion.
    Returns a new grammar (dict).
    """
    new_grammar = {}
    # We iterate over a copy, as we might add new keys (e.g., E')
    for nt, productions in list(grammar.items()):

        recursive_prods = []
        non_recursive_prods = []

        for prod in productions:
            if prod and prod[0] == nt:
                # This is a recursive production (A -> Aα)
                # We store the 'α' part
                recursive_prods.append(prod[1:])
            else:
                # This is a non-recursive production (A -> β)
                non_recursive_prods.append(prod)

        # If no recursion, just add the rules as-is
        if not recursive_prods:
            new_grammar[nt] = productions
            continue

        # --- If we are here, recursion was found! ---
        new_nt = f"{nt}'" # Create E'

        # Rule 1: A -> βA'
        # If no non-recursive rules, grammar is infinitely recursive.
        if not non_recursive_prods:
            # We can't fix this.
            raise ValueError(f"Non-terminal '{nt}' has left recursion but no non-recursive base case.")

        new_grammar[nt] = [prod + [new_nt] for prod in non_recursive_prods]

        # Rule 2: A' -> αA' | eps
        new_grammar[new_nt] = [prod + [new_nt] for prod in recursive_prods]
        new_grammar[new_nt].append(['eps'])

    return new_grammar

def grammar_to_string(grammar):
    """Helper to convert a grammar dict back to a string."""
    lines = []
    for nt, productions in grammar.items():
        rhs = " | ".join([" ".join(prod) for prod in productions])
        lines.append(f"{nt} -> {rhs}")
    return "\n".join(lines)