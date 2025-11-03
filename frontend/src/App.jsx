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

    // === 2. Handlers (Functions to call the API) ===

    const handleAnalyze = async () => {
        setIsLoading(true);
        setError(null);
        setAnalysis(null);      // Clear old results
        setParseResult(null); // Clear old results
        try {
            const response = await analyzeGrammar(grammarText);
            setAnalysis(response.data);
            if (response.data.conflicts && response.data.conflicts.length > 0) {
                // It's not an "error", but a "warning"
                setError("Grammar is not LL(1). Conflicts detected.");
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to analyze grammar.');
        }
        setIsLoading(false);
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