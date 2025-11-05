// frontend/src/App.jsx

import { useState } from 'react';
import { analyzeGrammar, parseString } from './api/backend';
import './App.css'; // We'll create this file next for styles
import AnalysisResults from './components/AnalysisResults';
import ParseOutput from './components/ParseOutput';
// --- Import Child Components (we will create these soon) ---
// import GrammarInput from './components/GrammarInput';
// import AnalysisResults from './components/AnalysisResults';
// import ParseRunner from './components/ParseRunner';
// import ParseOutput from './components/ParseOutput';

function App() {
    // === 1. State ===
    // User Inputs
    const [grammarText, setGrammarText] = useState('');
    const [inputString, setInputString] = useState('');

    // API Results
    const [analysis, setAnalysis] = useState(null); // { first, follow, table, conflicts, valid }
    const [parseResult, setParseResult] = useState(null); // { trace, tree, result }
    
    // UI State
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null); // To display API errors
    const [recursionError, setRecursionError] = useState(null);

    // === 2. Handlers (Functions to call the API) ===

    // frontend/src/App.jsx

const handleAnalyze = async () => {
    setIsLoading(true);
    setError(null);
    setAnalysis(null);
    setParseResult(null);
    setRecursionError(null); // <-- Clear previous error
    try {
        const response = await analyzeGrammar(grammarText);

        // --- THIS IS THE NEW LOGIC ---
        if (response.data.error_type === 'LEFT_RECURSION') {
            setRecursionError(response.data); // Save the fix data
            setError(response.data.analysis_error); // Show the error message
        } 
        // --- END NEW LOGIC ---
        else {
            // Happy path (no recursion)
            setAnalysis(response.data);
            if (response.data.conflicts && response.data.conflicts.length > 0) {
                setError("Grammar is not LL(1). Conflicts detected.");
            }
        }
    } catch (err) {
        setError(err.response?.data?.detail || 'Failed to analyze grammar.');
    }
    setIsLoading(false);
};

// frontend/src/App.jsx

// ... (after handleAnalyze)

const handleApplyFix = () => {
    if (!recursionError) return;

    // 1. Get the fixed grammar text from state
    const fixedGrammar = recursionError.repaired_grammar_text;

    // 2. Put that text into the main text area
    setGrammarText(fixedGrammar);

    // 3. Clear the error state
    setRecursionError(null);
    setError(null);

    // 4. We can now just let the user re-click "Analyze", 
    //    or we could trigger it automatically. Let's just update the text.
    //    The user will see the text change and can click "Analyze" again.
    //    This is a simple and clear UX.
};

    const handleParse = async () => {
        if (!analysis || !analysis.valid) {
             setError("Cannot parse: Grammar is not LL(1) or has not been analyzed.");
             return;
        }
        setIsLoading(true);
        setError(null);
        setParseResult(null); // Clear old parse results
        try {
            const response = await parseString(grammarText, inputString);
            setParseResult(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to parse string.');
        }
        setIsLoading(false);
    };

    // === 3. Render (The UI) ===
    return (
        <div className="app-container">
            <header className="app-header">
                <h1>LL(1) Parser Visualizer</h1>
                <p className="app-subtitle">Analyze grammars, inspect FIRST/FOLLOW, and visualize parse trees.</p>
            </header>

            <main className="app-main">
                {/* --- LEFT COLUMN (Inputs) --- */}
                <div className="input-panel">
                    <h3>1. Grammar Input</h3>
                    <textarea
                        className="grammar-textarea"
                        value={grammarText}
                        onChange={(e) => setGrammarText(e.target.value)}
                        placeholder="E -> T E'&#10;E' -> + T E' | eps&#10;T -> F T'&#10;..."
                    />
                    <button onClick={handleAnalyze} disabled={isLoading || !grammarText}>
                        {isLoading ? 'Analyzing...' : 'Analyze Grammar'}
                    </button>
                    {/* --- NEW UI BLOCK --- */}
{recursionError && (
    <div className="recursion-fix-box">
        <h4>Left Recursion Detected!</h4>
        <p>
            Your grammar has left recursion in: 
            <strong> {recursionError.recursive_non_terminals.join(', ')}</strong>.
        </p>
        <p>
            To make it LL(1) compatible, it must be rewritten. We can use
            this automatically generated equivalent:
        </p>
        <pre className="fixed-grammar-preview">
            {recursionError.repaired_grammar_text}
        </pre>
        <button onClick={handleApplyFix} className="fix-button">
            Use This Grammar
        </button>
    </div>
)}
{/* --- END NEW UI BLOCK --- */}
                    {/* --- Parse Runner Section --- */}
{analysis && analysis.valid && (
    <div className="parse-runner">
        <h4>2. Parse Input String</h4>
        <input
            type="text"
            className="parse-input"
            placeholder="e.g., id + id"
            value={inputString}
            onChange={(e) => setInputString(e.target.value)}
            disabled={isLoading}
        />
        <button
            onClick={handleParse}
            disabled={isLoading || !inputString}
        >
            {isLoading ? 'Parsing...' : 'Parse String'}
        </button>
    </div>
)}
                </div>

                {/* --- RIGHT COLUMN (Outputs) --- */}
                <div className="output-panel">
                    {/* Status Messages */}
                    {isLoading && <div className="loading-message">Loading...</div>}
                    {error && <div className="error-message">{error}</div>}

                    {/* Results */}
                    {/* We'll pass data to child components here */}
                    {/* {analysis && <AnalysisResults analysis={analysis} />} */}
                    {/* {parseResult && <ParseOutput result={parseResult} />} */}
                    {/* --- THIS IS THE NEW PART --- */}
                    {analysis && <AnalysisResults analysis={analysis} />}
                    {parseResult && <ParseOutput result={parseResult} />}
                    {/* Placeholder for now */}
                    {!isLoading && !error && !analysis && (
                        <div className="placeholder">
                            Enter a grammar and click "Analyze" to see the results.
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default App;