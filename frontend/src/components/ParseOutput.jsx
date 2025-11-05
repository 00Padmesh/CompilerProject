// frontend/src/components/ParseOutput.jsx

import React, { useState } from 'react';
import Tree from 'react-d3-tree';

// --- NEW COMPONENT: The Simulation Player ---
function SimulationPlayer({ steps }) {
    const [stepIndex, setStepIndex] = useState(0);
    const currentStep = steps[stepIndex];

    return (
        <div className="simulation-player">
            <div className="sim-state">
                <div className="sim-box">
                    <strong>Stack</strong>
                    <div className="sim-stack">
                        {/* Render stack top-to-bottom */
                        [...currentStep.stack].reverse().map((item, i) => (
                            <span key={i}>{item}</span>
                        ))}
                    </div>
                </div>
                <div className="sim-box">
                    <strong>Input</strong>
                    <div className="sim-input">
                        {currentStep.input.map((item, i) => (
                            <span key={i} className={i === 0 ? 'current-token' : ''}>
                                {item}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
            <div className="sim-action">
                <strong>Action:</strong> {currentStep.action}
            </div>
            <div className="sim-controls">
                <button 
                    onClick={() => setStepIndex(s => s - 1)} 
                    disabled={stepIndex === 0}
                >
                    Previous
                </button>
                <span>Step {stepIndex + 1} of {steps.length}</span>
                <button 
                    onClick={() => setStepIndex(s => s + 1)} 
                    disabled={stepIndex === steps.length - 1}
                >
                    Next
                </button>
            </div>
        </div>
    );
}

// --- UPDATED: Main ParseOutput Component ---
function ParseOutput({ result }) {
    // === CHANGE 1: Get `trace_steps` instead of `trace` ===
    const { trace_steps, parse_tree, result: status } = result;
    
    // === CHANGE 2: Default to the 'simulation' tab ===
    const [activeTab, setActiveTab] = useState('simulation');

    const statusClass = status.toLowerCase() === 'accepted' ? 'status-accepted' : 'status-rejected';

    // === CHANGE 3: Create the old trace from the new data ===
    const fullTrace = trace_steps
        .map(step => `Stack: [${step.stack.join(', ')}] | Input: [${step.input.join(', ')}] | Action: ${step.action}`)
        .join('\n');

    return (
        <div className="parse-output-container">
            <h3>Parse Result</h3>
            <div className={`parse-status ${statusClass}`}>
                <strong>Status:</strong> {status}
            </div>

            {/* === CHANGE 4: Add the "Simulation" tab === */}
            <div className="tab-nav">
                <button 
                    className={activeTab === 'simulation' ? 'active' : ''}
                    onClick={() => setActiveTab('simulation')}
                >
                    Simulation
                </button>
                <button 
                    className={activeTab === 'tree' ? 'active' : ''}
                    onClick={() => setActiveTab('tree')}
                >
                    Parse Tree
                </button>
                <button 
                    className={activeTab === 'trace' ? 'active' : ''}
                    onClick={() => setActiveTab('trace')}
                >
                    Parse Trace
                </button>
            </div>

            <div className="tab-content">
                {/* === CHANGE 5: Add the SimulationPlayer content === */}
                {activeTab === 'simulation' && (
                    <SimulationPlayer steps={trace_steps} />
                )}

                {activeTab === 'tree' && (
                    <div className="tree-container">
                        <div style={{ width: '100%', height: '600px', border: '1px solid #ddd' }}>
                            <Tree 
                                data={parse_tree} 
                                // ... (all other props are the same)
                                orientation="vertical"
                                pathFunc="step"
                                translate={{ x: 300, y: 50 }}
                                collapsible={true}
                                separation={{ siblings: 1, nonSiblings: 1.5 }}
                            />
                        </div>
                    </div>
                )}

                {activeTab === 'trace' && (
                    <div className="trace-container">
                        {/* === CHANGE 6: Use the generated `fullTrace` === */}
                        <pre className="parse-trace">
                            {fullTrace}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ParseOutput;