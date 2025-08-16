import React, { useCallback } from 'react';
import ReactFlow, { Background, Controls, MiniMap } from 'react-flow-renderer';

const nodes = [
  { id: '1', type: 'default', position: { x: 300, y: 150 }, data: { label: 'Cosmic Chain Protocol', details: 'Validator-free blockchain with entropy burns, cycle resets, and quantum readiness; no hard cap.', logic: 'Combines micro PoW/PoS consensus, automatic burns, and ERA resets for self-regulation.', reason: 'Mimics cosmic entropy to prune stagnation, ensuring a dynamic, sustainable ecosystem for long-term use.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '3px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 15px #00ffff' } },
  { id: '2', position: { x: 300, y: 250 }, data: { label: 'Block Emission', details: 'Generates blocks every 10 minutes, starting the validation cycle.', logic: 'Continuous emission sustains network activity with random queue for fairness.', reason: 'Drives perpetual motion like cosmic expansion, preventing stagnation while controlling supply.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 10px #00ffff' } },
  { id: '3', position: { x: 300, y: 350 }, data: { label: 'Validation', details: 'Multi-step process to confirm block integrity without external validators.', logic: 'Sequences entry, fee reservation, queuing, and dual consensus for secure processing.', reason: 'Ensures network security and fairness, punishing low effort to maintain entropy.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 10px #00ffff' } },
  { id: '3.1', position: { x: 300, y: 450 }, data: { label: '1. Block Entered', details: 'Block submitted to the network for validation initiation.', logic: 'Marks entry into the consensus pipeline via node submission.', reason: 'Triggers the protocol\'s self-regulating mechanisms, aligning with adaptive flow.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '3.2', position: { x: 300, y: 550 }, data: { label: '2. Fees Reserved', details: 'Small transaction fees held from the proposing node’s wallet pending validation outcome.', logic: 'Reserves fees as a stake from the proposer; refunded on success or burned on failure.', reason: 'Incentivizes commitment, enforcing entropy by penalizing failures.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '3.3', position: { x: 300, y: 650 }, data: { label: '3. Orbital Queue', details: 'Blocks queued in random order for processing.', logic: 'Uses randomized orbit-like queue to prevent manipulation.', reason: 'Ensures fairness and reduces spam, mimicking cosmic randomness.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '3.4', position: { x: 300, y: 750 }, data: { label: '4. Micro PoW-PoS', details: 'Hybrid micro Proof of Work and Proof of Stake consensus.', logic: 'Validates blocks through computational PoW and stake-based PoS.', reason: 'Secures network without validators, distributing rewards to active participants.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '3.5', position: { x: 500, y: 800 }, data: { label: '5. Success', details: 'Block added to chain, fees refunded, reward issued.', logic: 'Confirms integrity, releases fees, and allocates reward to submitter.', reason: 'Rewards accuracy, encouraging motion and network health.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '3.6', position: { x: 100, y: 800 }, data: { label: '6. Failure', details: 'Block burned, fees charged as penalty.', logic: 'Fails validation, triggers Blackhole Burn, forfeits fees.', reason: 'Deters spam/low effort, enforcing entropy to prune inefficiency.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '4', position: { x: 300, y: 950 }, data: { label: 'Burn Mechanisms', details: 'Entropy-driven pathways for permanent coin burns and allocation.', logic: 'Applies burns from inactivity, failures, resets, and dust, with 25% splits post-allocation.', reason: 'Preserves motion by punishing stagnation, balancing supply dynamically.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 10px #00ffff' } },
  { id: '4.1', position: { x: 100, y: 1050 }, data: { label: 'Inactivity', details: '2% annual decay after 5 years, 50% burn at 20 years (50% split).', logic: 'Reduces dormant wallet balances over time, reallocating remainder.', reason: 'Prunes idle resources, enforcing entropy like cosmic decay.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '4.2', position: { x: 300, y: 1050 }, data: { label: 'Failed Burn', details: 'Small burn from miners/stakers on validation failure.', logic: 'Penalizes failed attempts post-consensus check.', reason: 'Ensures participation quality, reducing network bloat.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '4.4', position: { x: 500, y: 1050 }, data: { label: 'Dust', details: 'Burns sub-tradable micro-balances below threshold.', logic: 'Periodically eliminates unusable dust to clean the chain.', reason: 'Improves efficiency, eliminating noise like cosmic dust.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '4.5', position: { x: 300, y: 1150 }, data: { label: 'Cosmic Labs', details: 'Administers 100% burn allocation from inactivity lifecycle.', logic: 'Distributes inactivity burn proceeds: 50% Burnt Forever, 25% Circulation, 25% Cosmic Labs.', reason: 'Funds development and sustains circulation without governance, supporting protocol evolution.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 10px #00ffff' } },
  { id: '4.5.1', position: { x: 100, y: 1250 }, data: { label: 'Burnt Forever (50%)', details: 'Permanently removed from supply.', logic: 'Burns 50% of inactivity proceeds to reduce total coins.', reason: 'Controls supply, enhancing scarcity through entropy.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '4.5.2', position: { x: 300, y: 1250 }, data: { label: 'Circulation (25%)', details: 'Reintegrated into circulating supply.', logic: 'Recycles 25% of inactivity proceeds to boost liquidity.', reason: 'Sustains economic activity without inflation.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '4.5.3', position: { x: 500, y: 1250 }, data: { label: 'Cosmic Labs (25%)', details: 'Allocated for R&D and operational needs.', logic: 'Directs 25% of inactivity proceeds to Cosmic Labs as non-governing entity.', reason: 'Enables tooling, audits, and QLE migration for long-term viability.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
  { id: '5', position: { x: 0, y: 150 }, data: { label: 'Quantum Leap', details: 'Migration to post-quantum cryptography (Kyber/Dilithium).', logic: 'Upgrades during QLE windows with transitional tools.', reason: 'Prepares for quantum threats, ensuring eternal security.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 10px #00ffff' } },
  { id: '6', position: { x: 600, y: 150 }, data: { label: 'ERA Reset', details: 'Resets reward to 25 COS when reward ≤1 COS, applied only after the end of the ongoing ERA (1st ERA: 1460 days, subsequent: 1095 days). Other elements (supply, burns) remain unchanged.', logic: 'Triggers a cycle reset by burning old economic assumptions, with ERA-end application providing a predictable upgrade window for miners.', reason: 'Renews miner incentives like a cosmic rebirth, ensuring sustainability without disrupting existing balances.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 10px #00ffff' } },
  { id: '6.1', position: { x: 600, y: 250 }, data: { label: 'Reward Halving', details: 'Halves reward every 210,000 blocks, applied only after the end of the ongoing ERA (1st ERA: 1460 days, subsequent: 1095 days). Other elements (supply, burns) remain unchanged.', logic: 'Reduces reward based on block count, with ERA-end application offering miners a predictable adjustment period.', reason: 'Controls supply naturally without hard caps, aligning with cosmic entropy while preserving ecosystem stability.' }, style: { background: '#1a1a3a', color: '#e0e0ff', border: '2px solid #00ffff', borderRadius: '10px', width: '200px', height: '80px', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 8px #00ffff' } },
];

const edges = [
  { id: 'e1', source: '1', target: '2', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e2', source: '2', target: '3', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e3', source: '3', target: '3.1', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e4', source: '3.1', target: '3.2', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e5', source: '3.2', target: '3.3', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e6', source: '3.3', target: '3.4', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e7', source: '3.4', target: '3.5', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e8', source: '3.4', target: '3.6', animated: true, style: { stroke: '#ff8800', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e9', source: '3', target: '4', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e10', source: '4', target: '4.1', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e11', source: '4', target: '4.2', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e12', source: '4', target: '4.4', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e13', source: '4', target: '4.5', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e14', source: '4.5', target: '4.5.1', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e15', source: '4.5', target: '4.5.2', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e16', source: '4.5', target: '4.5.3', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e17', source: '4.5', target: '4.5.4', animated: true, style: { stroke: '#ff8800', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e18', source: '1', target: '5', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e19', source: '1', target: '6', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e20', source: '6', target: '6.1', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
  { id: 'e21', source: '1', target: '7', animated: true, style: { stroke: '#00ffff', markerEnd: 'url(#arrowhead)' }, type: 'smoothstep' },
];

const onNodeClick = (event, node) => {
  alert(`Node: ${node.data.label}\nDetails: ${node.data.details || 'No additional details available'}\nLogic: ${node.data.logic || 'No logic available'}\nReason: ${node.data.reason || 'No reason available'}`);
};

const App = () => {
  return (
    <div style={{ height: '100vh', background: 'linear-gradient(135deg, #0a0a1f, #1a1a3a)' }}>
      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#00ffff" />
          </marker>
        </defs>
      </svg>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodeClick={onNodeClick}
        fitView
      >
        <Background variant="dots" color="#00ffff" />
        <Controls />
        <MiniMap />
      </ReactFlow>
      <p style={{ color: '#00ffff', textAlign: 'center', position: 'absolute', bottom: '10px', width: '100%' }}>
        Note: Check the simulation for dynamic insights.
      </p>
    </div>
  );
};

export default App;