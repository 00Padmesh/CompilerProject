# first_follow.py

def compute_first(grammar):
    """
    Compute FIRST sets for all non-terminals in the grammar.
    """
    first = {nt: set() for nt in grammar}
    terminals = {
        sym
        for prods in grammar.values()
        for prod in prods
        for sym in prod
        if sym not in grammar and sym != 'eps'
    }

    # Initialize with terminals
    for t in terminals:
        first[t] = {t}

    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for production in productions:
                # Rule: For X -> Y1 Y2 ... Yk
                for symbol in production:
                    # All of FIRST(Y1) - {eps} is in FIRST(X)
                    first_y = first.get(symbol, {symbol}) # Handles terminals directly
                    
                    before_len = len(first[nt])
                    first[nt].update(first_y - {'eps'})
                    if len(first[nt]) > before_len:
                        changed = True

                    # If eps not in FIRST(Y1), then we stop.
                    if 'eps' not in first_y:
                        break
                else:
                    # If we finished the loop (all symbols' FIRST sets contained eps)
                    # then add eps to FIRST(X)
                    before_len = len(first[nt])
                    first[nt].add('eps')
                    if len(first[nt]) > before_len:
                        changed = True
    
    # Remove terminals from the final dictionary if they were added
    final_first = {k: v for k, v in first.items() if k in grammar}
    return final_first

def _first_of_sequence(sequence, first_sets):
    """Helper to compute FIRST set for a sequence of symbols (e.g., beta)."""
    result = set()
    for symbol in sequence:
        symbol_first = first_sets.get(symbol, {symbol})
        result.update(symbol_first - {'eps'})
        if 'eps' not in symbol_first:
            return result
    # If we get through the whole loop, it means all symbols can be eps
    result.add('eps')
    return result


def compute_follow(grammar, first, start_symbol):
    """
    Compute FOLLOW sets for all non-terminals.
    """
    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for A, productions in grammar.items():
            for production in productions:
                for i, B in enumerate(production):
                    if B in grammar:  # B must be a non-terminal
                        beta = production[i + 1:]
                        
                        before_len = len(follow[B])

                        if beta:
                            # Rule 2: FOLLOW(B) contains FIRST(beta) - {eps}
                            first_beta = _first_of_sequence(beta, first)
                            follow[B].update(first_beta - {'eps'})

                            # Rule 3: If FIRST(beta) contains eps, FOLLOW(B) contains FOLLOW(A)
                            if 'eps' in first_beta:
                                follow[B].update(follow[A])
                        else:
                            # Rule 3: For A -> alpha B, FOLLOW(B) contains FOLLOW(A)
                            follow[B].update(follow[A])

                        if len(follow[B]) > before_len:
                            changed = True
    return follow


# Example usage
if __name__ == "__main__":
    from grammar_utils import read_grammar

    grammar = read_grammar("tests/sample_grammar.txt")
    start_symbol = list(grammar.keys())[0]

    first = compute_first(grammar)
    follow = compute_follow(grammar, first, start_symbol)

    print("FIRST sets:")
    for nt, s in first.items():
        print(f"FIRST({nt}) = {s}")

    print("\nFOLLOW sets:")
    for nt, s in follow.items():
        print(f"FOLLOW({nt}) = {s}")
