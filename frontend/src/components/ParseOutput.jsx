// frontend/src/components/ParseOutput.jsx

import React, { useState } from 'react';
import Tree from 'react-d3-tree';

// This is the "magic" - the data from your Python backend is already
// in the format { name: "...", children: [...] } that this library needs.

function ParseOutput({ result }) {
    const { trace, parse_tree, result: status } = result;
    const [activeTab, setActiveTab] = useState('tree');

    // Get the status (Accepted/Rejected) and apply a CSS class
    const statusClass = status.toLowerCase() === 'accepted' ? 'status-accepted' : 'status-rejected';

    return (
        <div className="parse-output-container">
            <h3>Parse Result</h3>
            
            <div className={`parse-status ${statusClass}`}>
                <strong>Status:</strong> {status}
            </div>

            {/* --- Tab Navigation --- */}
            <div className="tab-nav">
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

            {/* --- Tab Content --- */}
            <div className="tab-content">
                {activeTab === 'tree' && (
                    <div className="tree-container">
                        {/* IMPORTANT: react-d3-tree *must* be in a container
                          with a defined height, or it will not be visible.
                        */}
                        <div style={{ width: '100%', height: '600px', border: '1px solid #ddd' }}>
                            <Tree 
                                data={parse_tree} 
                                orientation="vertical"
                                pathFunc="step" // Gives 90-degree angles
                                translate={{ x: 300, y: 50 }} // Centers the initial root node
                                collapsible={true} // Allow collapsing nodes
                                separation={{ siblings: 1, nonSiblings: 1.5 }}
                            />
                        </div>
                    </div>
                )}

                {activeTab === 'trace' && (
                    <div className="trace-container">
                        <pre className="parse-trace">
                            {trace.join('\n')}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ParseOutput;