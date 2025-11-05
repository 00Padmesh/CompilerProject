from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from grammar_utils import read_grammar
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
    """
    Input: Grammar text (string)
    Output: FIRST, FOLLOW, Parsing Table, and conflict status
    """
    try:
        grammar = read_grammar(data.grammar_text)
        start_symbol = list(grammar.keys())[0]

        first = compute_first(grammar)
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
        raise HTTPException(status_code=400, detail=f"Invalid grammar: {str(e)}")


@app.post("/parse")
def parse_string(data: ParseInput):
    """
    Input: Grammar + input string
    Output: Parsing trace, parse tree, and result (Accepted/Rejected)
    """
    try:
        grammar = read_grammar(data.grammar_text)
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
