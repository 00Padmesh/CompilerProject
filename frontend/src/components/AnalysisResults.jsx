// frontend/src/components/AnalysisResults.jsx

import React from 'react';

/**
 * Renders a table for FIRST or FOLLOW sets.
 * @param {string} title - "FIRST Sets" or "FOLLOW Sets"
 * @param {object} sets - The { 'A': ['a', 'b'], ... } object
 */
function renderSetTable(title, sets) {
  const nonTerminals = Object.keys(sets).sort();

  return (
    <div className="set-table-container">
      <h3>{title}</h3>
      <table className="results-table">
        <thead>
          <tr>
            <th>Non-Terminal</th>
            <th>Set</th>
          </tr>
        </thead>
        <tbody>
          {nonTerminals.map(nt => (
            <tr key={nt}>
              <td>{nt}</td>
              <td>{`{ ${sets[nt].join(', ')} }`}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/**
 * Renders the main LL(1) Parsing Table.
 * @param {object} parsingTable - The parsing_table object
 * @param {object} followSets - The follow sets (to get all terminals)
 * @param {Array} conflicts - The list of conflicts for highlighting
 */
function renderParsingTable(parsingTable, followSets, conflicts) {
  const nonTerminals = Object.keys(parsingTable).sort();
  
  // Get all terminals and '$' from the table keys and FOLLOW sets
  const terminals = new Set();
  nonTerminals.forEach(nt => {
    Object.keys(parsingTable[nt]).forEach(t => terminals.add(t));
  });
  Object.values(followSets).forEach(set => {
    set.forEach(t => terminals.add(t));
  });

  // Ensure '$' is last
  const tableHeaders = [
    ...Array.from(terminals).filter(t => t !== '$').sort(),
    '$'
  ];

  return (
    <div className="parsing-table-container">
      <h3>LL(1) Parsing Table</h3>
      <div className="table-wrapper"> {/* For horizontal scrolling on small screens */}
        <table className="results-table parsing-table">
          <thead>
            <tr>
              <th>NT \ T</th>
              {tableHeaders.map(t => <th key={t}>{t}</th>)}
            </tr>
          </thead>
          <tbody>
            {nonTerminals.map(nt => (
              <tr key={nt}>
                <td>{nt}</td>
                {tableHeaders.map(terminal => {
                  const production = parsingTable[nt][terminal];
                  // Check if this cell has a conflict
                  const isConflict = conflicts.some(c => c[0] === nt && c[1] === terminal);
                  const cellText = production ? `${nt} → ${production.join(' ')}` : ' ';

                  return (
                    <td key={terminal} className={isConflict ? 'conflict-cell' : ''}>
                      {cellText}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/**
 * Renders the list of conflicts, if any.
 * @param {Array} conflicts - The list of conflicts
 */
function renderConflicts(conflicts) {
  if (!conflicts || conflicts.length === 0) {
    return (
      <div className="conflicts-container conflicts-valid">
        <strong>Grammar is LL(1).</strong> No conflicts found.
      </div>
    );
  }

  return (
    <div className="conflicts-container conflicts-invalid">
      <strong>GramMAR IS NOT LL(1)</strong>
      <p>The following conflicts were detected:</p>
      <ul className="conflicts-list">
        {conflicts.map((conflict, index) => {
          const [nt, terminal, existing, newProd, type] = conflict;
          return (
            <li key={index} className="conflict-item">
              <strong>{type} Conflict on [ {nt}, {terminal} ]:</strong>
              <div>Existing: <code>{nt} → {existing.join(' ')}</code></div>
              <div>New: <code>{nt} → {newProd.join(' ')}</code></div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}


// --- Main Component ---
function AnalysisResults({ analysis }) {
  if (!analysis) return null;

  const { first, follow, parsing_table, conflicts } = analysis;

  return (
    <div className="analysis-results">
      
      {/* 1. Conflicts */}
      {renderConflicts(conflicts)}

      {/* 2. FIRST & FOLLOW Sets */}
      <div className="sets-container">
        {first && renderSetTable("FIRST Sets", first)}
        {follow && renderSetTable("FOLLOW Sets", follow)}
      </div>

      {/* 3. Parsing Table */}
      {parsing_table && renderParsingTable(parsing_table, follow, conflicts)}
      
    </div>
  );
}

export default AnalysisResults;