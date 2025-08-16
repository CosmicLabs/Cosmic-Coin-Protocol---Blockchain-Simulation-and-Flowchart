# Cosmic Coin Protocol

## Simulation
Streamlit app reads `Adaptive_Scarcity_Coin_Model_With_Formulas.xlsx`, builds a per-block schedule from the ERA table, time-compresses into a demo (e.g., 20 min, 10-sec blocks). See: rewards (25 COS halved per ERA), burns, inactivity decay, Quantum trigger.

## Overview
Validator-free blockchain with entropy burns & micro PoW/PoS, no hard cap. Blocks every 10 min, queued randomly to curb spam. Rewards start 25 COS, halve each 210k blocks, reset if ≤1 COS. Failures & inactivity trigger burns (50% destroyed, 25% recirculated, 25% to R&D). Quantum-ready (Kyber/Dilithium). Dynamic, ever-moving, not deflationary.

## Run Locally
- Flowchart: `cd flowchart/cosmic_chain_flowchart_react && npm start`
- Simulation: `cd simulation && streamlit run cosmic_chain_simulation.py` (upload Excel)

## Deployed
- Flowchart: [TBD](https://CosmicLabs.github.io/cosmic-chain-protocol)
- Simulation: [TBD](https://share.streamlit.io/CosmicLabs/cosmic-chain-protocol/simulation)

## Contact
genesis@cosmicycle.com

## Credits
Cosmic Labs Team
