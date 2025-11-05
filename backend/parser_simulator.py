# parser_simulator.py
from grammar_utils import read_grammar
from first_follow import compute_first, compute_follow
from parsing_table import compute_parsing_table


# backend/parser_simulator.py

def parse_input_string(grammar, parsing_table, start_symbol, input_string):
    input_tokens = input_string.split() + ['$']
    stack = ['$', start_symbol]
    pointer = 0
    
    # === CHANGE 1: Rename `trace` to `trace_steps` ===
    trace_steps = [] 
    
    parse_tree = {"name": start_symbol, "children": []}
    tree_stack = [parse_tree]

    while stack:
        # --- Capture state at the *beginning* of the loop ---
        # We use list() to make a snapshot copy of the stack
        current_stack = list(stack) 
        current_input = input_tokens[pointer:]

        top = stack.pop()
        current_token = input_tokens[pointer] if pointer < len(input_tokens) else None

        # --- This is the data we will append ---
        step_data = {
            "stack": current_stack[::-1], # Reversed for user-friendly view
            "input": current_input,
            "action": "" # We'll fill this in
        }

        # Match terminal
        if top == current_token:
            step_data["action"] = f"Match '{current_token}'"
            trace_steps.append(step_data)
            
            pointer += 1
            if tree_stack:
                tree_stack.pop()

        # Epsilon production
        elif top == 'eps':
            step_data["action"] = f"Expand {top} → ε"
            trace_steps.append(step_data)

            if tree_stack:
                tree_stack.pop()

        # Error: No rule
        elif top not in parsing_table or current_token not in parsing_table[top]:
            step_data["action"] = f"ERROR: No rule for M[{top}, {current_token}]"
            trace_steps.append(step_data)
            return trace_steps, parse_tree, "Rejected"

        # Expand using parsing table
        else:
            production = parsing_table[top][current_token]
            rhs = production if production != ['eps'] else []
            
            step_data["action"] = f"Expand {top} → {' '.join(production)}"
            trace_steps.append(step_data)

            current_node = tree_stack.pop() if tree_stack else None

            if current_node:
                current_node["children"] = [{"name": sym, "children": []} for sym in production]
                for child in reversed(current_node["children"]):
                    if child["name"] != 'eps':
                        stack.append(child["name"])
                        tree_stack.append(child)
            else:
                for sym in reversed(rhs):
                    if sym != 'eps':
                        stack.append(sym)

    # === CHANGE 2: Add the final "Accepted" state ===
    trace_steps.append({
        "stack": ["$"],
        "input": ["$"],
        "action": "Accepted"
    })
    
    status = "Accepted"
    
    # === CHANGE 3: Return `trace_steps` ===
    return trace_steps, parse_tree, status

# ... rest of the file ...


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
