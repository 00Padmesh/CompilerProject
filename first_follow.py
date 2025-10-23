from grammar_utils import read_grammar

def compute_first(grammar):
    first = {nt: set() for nt in grammar}
    
    def first_of(symbol):
        if symbol not in grammar:
            return {symbol} if symbol != 'ε' else {'ε'}

        result = set()
        for production in grammar[symbol]:
            for sym in production:
                res = first_of(sym)
                result |= (res - {'ε'})
                if 'ε' not in res:
                    break
            else:
                result.add('ε')
        return result

    changed = True
    while changed:
        changed = False
        for nt in grammar:
            before = len(first[nt])
            for production in grammar[nt]:
                for sym in production:
                    first[nt] |= (first_of(sym) - {'ε'})
                    if 'ε' not in first_of(sym):
                        break
                else:
                    first[nt].add('ε')
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
                                # handle terminals properly
                                if sym in grammar:
                                    first_beta |= first[sym]
                                    if 'ε' not in first[sym]:
                                        break
                                else:  # terminal
                                    first_beta.add(sym)
                                    break
                            else:
                                first_beta.add('ε')
                            
                            before = len(follow[B])
                            follow[B] |= (first_beta - {'ε'})
                            if 'ε' in first_beta:
                                follow[B] |= follow[A]
                            if len(follow[B]) > before:
                                changed = True
                        else:
                            before = len(follow[B])
                            follow[B] |= follow[A]
                            if len(follow[B]) > before:
                                changed = True
    return follow




g = read_grammar("tests/sample_grammars.txt")
first = compute_first(g)
print("First sets: ")
print(first)

start_symbol = list(g.keys())[0]  # pick the first non-terminal as start
follow = compute_follow(g, first, start_symbol=start_symbol)
print("\nFollow sets: ")
print(follow)
