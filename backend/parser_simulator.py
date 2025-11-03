# parser_simulator.py
from grammar_utils import read_grammar
from first_follow import compute_first, compute_follow
from parsing_table import compute_parsing_table


def parse_input_string(grammar, parsing_table, start_symbol, input_string):
    input_tokens = input_string.split() + ['$']
    stack = ['$', start_symbol]
    pointer = 0
    trace = []
    parse_tree = {"name": start_symbol, "children": []}
    tree_stack = [parse_tree]

    while stack:
        top = stack.pop()
        current_token = input_tokens[pointer] if pointer < len(input_tokens) else None

        # Match terminal
        if top == current_token:
            trace.append(
                f"Stack: {stack[::-1]} | Input: {' '.join(input_tokens[pointer:])} | "
                f"Action: Match '{current_token}'"
            )
            pointer += 1
            if tree_stack:
                tree_stack.pop()

        # Epsilon production
        elif top == 'eps':
            trace.append(
                f"Stack: {stack[::-1]} | Input: {' '.join(input_tokens[pointer:])} | "
                f"Action: Expand {top} → ε"
            )
            if tree_stack:
                tree_stack.pop()

        # Error: No rule for this combination
        elif top not in parsing_table or current_token not in parsing_table[top]:
            trace.append(
                f"Stack: {stack[::-1]} | Input: {' '.join(input_tokens[pointer:])} | "
                f"Action: ERROR (no rule for {top}, {current_token})"
            )
            return trace, parse_tree, "Rejected"

        # Expand using parsing table
        else:
            production = parsing_table[top][current_token]
            rhs = production if production != ['eps'] else []
            trace.append(
                f"Stack: {stack[::-1]} | Input: {' '.join(input_tokens[pointer:])} | "
                f"Action: Expand {top} → {' '.join(production)}"
            )

            current_node = tree_stack.pop() if tree_stack else None

            if current_node:
                current_node["children"] = [{"name": sym, "children": []} for sym in production]

                # Push children (in reverse order for correct left-to-right traversal)
                for child in reversed(current_node["children"]):
                    if child["name"] != 'eps':
                        stack.append(child["name"])
                        tree_stack.append(child)
            else:
                # If we somehow lost sync, continue safely
                for sym in reversed(rhs):
                    if sym != 'eps':
                        stack.append(sym)

    # Final acceptance check
    status = "Accepted" if pointer == len(input_tokens) else "Rejected"
    return trace, parse_tree, status


if __name__ == "__main__":
    grammar = read_grammar("tests/sample_grammar.txt")
    start_symbol = list(grammar.keys())[0]

    first = compute_first(grammar)
    follow = compute_follow(grammar, first, start_symbol)
    parsing_table, conflicts = compute_parsing_table(grammar, first, follow)

    input_str = "id + id * id"
    print("\n=== Parsing Trace ===")
    trace, tree, result = parse_input_string(grammar, parsing_table, start_symbol, input_str)
    for step in trace:
        print(step)
    print("=====================\n")

    print(f"Result: {result}\n")

    import json
    print("=== Parse Tree ===")
    print(json.dumps(tree, indent=2))
