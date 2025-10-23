# first_follow.py

def compute_first(grammar):
    first = {nt: set() for nt in grammar}

    def first_of(symbol):
        if symbol not in grammar:
            return {symbol} if symbol != 'eps' else {'eps'}

        result = set()
        for production in grammar[symbol]:
            for sym in production:
                res = first_of(sym)
                result |= (res - {'eps'})
                if 'eps' not in res:
                    break
            else:
                result.add('eps')
        return result

    changed = True
    while changed:
        changed = False
        for nt in grammar:
            before = len(first[nt])
            for production in grammar[nt]:
                for sym in production:
                    first[nt] |= (first_of(sym) - {'eps'})
                    if 'eps' not in first_of(sym):
                        break
                else:
                    first[nt].add('eps')
            after = len(first[nt])
            if after > before:
                changed = True
    return first


def compute_follow(grammar, first, start_symbol):
    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add('$')  # End of input marker

    changed = True
    while changed:
        changed = False
        for A in grammar:
            for production in grammar[A]:
                for i, B in enumerate(production):
                    if B in grammar:  # B is a non-terminal
                        beta = production[i+1:]
                        if beta:
                            first_beta = set()
                            for sym in beta:
                                if sym in grammar:
                                    first_beta |= first[sym]
                                    if 'eps' not in first[sym]:
                                        break
                                else:
                                    first_beta.add(sym)
                                    break
                            else:
                                first_beta.add('eps')

                            before = len(follow[B])
                            follow[B] |= (first_beta - {'eps'})
                            if 'eps' in first_beta:
                                follow[B] |= follow[A]
                            if len(follow[B]) > before:
                                changed = True
                        else:
                            before = len(follow[B])
                            follow[B] |= follow[A]
                            if len(follow[B]) > before:
                                changed = True
    return follow


# Example usage
if __name__ == "__main__":
    from grammar_utils import read_grammar, find_symbols

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