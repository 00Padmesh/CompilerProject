// frontend/src/api/backend.js
import axios from 'axios';

// Create an Axios instance pointing to your FastAPI backend
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000', // Your FastAPI server address
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Analyzes the grammar text.
 * @param {string} grammarText The raw grammar string.
 *entry {Promise<object>} The analysis result (FIRST, FOLLOW, table, conflicts).
 */
export const analyzeGrammar = (grammarText) => {
    // The data is wrapped in an object as defined by your Pydantic model
    return apiClient.post('/analyze', { grammar_text: grammarText });
};

/**
 * Parses an input string with the given grammar.
 * @param {string} grammarText The raw grammar string.
 * @param {string} inputString The input string to parse.
 * @returns {Promise<object>} The parse result (trace, tree, status).
 */
export const parseString = (grammarText, inputString) => {
    return apiClient.post('/parse', {
        grammar_text: grammarText,
        input_string: inputString,
    });
};