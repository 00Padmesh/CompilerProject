from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from grammar_utils import read_grammar, find_symbols, detect_direct_left_recursion
from grammar_rewriter import eliminate_direct_left_recursion, grammar_to_string
from first_follow import compute_first, compute_follow
from parsing_table import compute_parsing_table
from parser_simulator import parse_input_string

app = FastAPI(title="LL(1) Parser API", version="1.0")

# ✅ Allow frontend requests (React/JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later to localhost:5173 etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 📍 Models
# -------------------------------
class GrammarInput(BaseModel):
    grammar_text: str


class ParseInput(BaseModel):
    grammar_text: str
    input_string: str


# -------------------------------
# 📍 Routes
# -------------------------------
@app.get("/")
def home():
    return {"message": "LL(1) Parser Backend is running."}


@app.post("/analyze")
def analyze_grammar(data: GrammarInput):
    try:
        grammar = read_grammar(data.grammar_text)
        recursive_rules = detect_direct_left_recursion(grammar)

        # --- THIS IS THE NEW LOGIC ---
        if recursive_rules:
            fixed_grammar = eliminate_direct_left_recursion(grammar)
            fixed_grammar_text = grammar_to_string(fixed_grammar)

            # Return a special response telling the frontend about the problem AND the fix
            return {
                "analysis_error": "Direct left recursion detected.",
                "error_type": "LEFT_RECURSION",
                "recursive_non_terminals": recursive_rules,
                "repaired_grammar_text": fixed_grammar_text
            }
        # --- END NEW LOGIC ---

        # If no recursion, proceed as normal
        start_symbol = list(grammar.keys())[0]
        first = compute_first(grammar)
        # ... (rest of the function)
        follow = compute_follow(grammar, first, start_symbol)
        parsing_table, conflicts = compute_parsing_table(grammar, first, follow)
        return {
            "grammar": grammar,
            "first": first,
            "follow": follow,
            "parsing_table": parsing_table,
            "conflicts": conflicts,
            "valid": len(conflicts) == 0
        }

    except Exception as e:
        # Catch our ValueError from the rewriter
        if isinstance(e, ValueError):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=400, detail=f"Invalid grammar: {str(e)}")


@app.post("/parse")
def parse_string(data: ParseInput):
    """
    Input: Grammar + input string
    Output: Parsing trace, parse tree, and result (Accepted/Rejected)
    """
    try:
        grammar = read_grammar(data.grammar_text)
        recursive_rules = detect_direct_left_recursion(grammar)
        if recursive_rules:
            raise HTTPException(
                status_code=400, 
                detail=f"Grammar is not LL(1): Direct left recursion detected in non-terminal(s): {', '.join(recursive_rules)}"
            )
        # --- END OF BLOCK ---
        start_symbol = list(grammar.keys())[0]

        first = compute_first(grammar)
        follow = compute_follow(grammar, first, start_symbol)
        parsing_table, conflicts = compute_parsing_table(grammar, first, follow)

        if conflicts:
            raise HTTPException(...)

        # === CHANGE 4: Update variable names ===
        trace_steps, tree, status = parse_input_string(grammar, parsing_table, start_symbol, data.input_string)
        
        # === CHANGE 5: Update the return object key ===
        return {
            "trace_steps": trace_steps, # Renamed from "trace"
            "parse_tree": tree,
            "result": status
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during parsing: {str(e)}")


# -------------------------------
# 🚀 Run locally: uvicorn main:app --reload
# -------------------------------
