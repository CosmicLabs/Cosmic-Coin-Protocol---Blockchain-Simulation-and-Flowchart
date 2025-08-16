import streamlit as st
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS for dark cosmic theme with neon accents
st.markdown("""
    <style>
    .stApp { background-color: #0a0a1f; color: #e0e0ff; }
    h1 { color: #00ffff; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; animation: glow 2s infinite alternate; }
    @keyframes glow { from { text-shadow: 0 0 5px #00ffff; } to { text-shadow: 0 0 15px #00ffff, 0 0 25px #00ffff; } }
    .stButton > button { background-color: #1a1a3a; color: #00ffff; border: 1px solid #00ffff; box-shadow: 0 0 5px #00ffff; }
    .stButton > button:hover { box-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; }
    .stProgress > div > div > div > div { background-color: #00ffff; }
    .metric-box { background-color: #1a1a3a; padding: 10px; border-radius: 5px; border: 1px solid #00ffff; box-shadow: 0 0 5px #00ffff; margin: 5px; text-align: center; height: 80px; display: flex; align-items: center; justify-content: center; font-size: 14px; }
    .log-entry-pass { color: #00ff00; }
    .log-entry-fail { color: #ff0000; }
    .log-entry-burn { color: #ff8800; }
    .log-entry-reset { color: #ff00ff; }
    .log-entry-quantum { color: #00ffff; }
    .orb { display: inline-block; width: 20px; height: 20px; background-color: #00ffff; border-radius: 50%; animation: pulse 1s infinite alternate; margin: 5px; position: relative; }
    .orb::after { content: attr(data-block); position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 10px; color: #000000; }
    @keyframes pulse { from { transform: scale(1); opacity: 1; } to { transform: scale(1.2); opacity: 0.7; } }
    .blackhole { display: inline-block; width: 20px; height: 20px; background-color: #ff8800; border-radius: 50%; animation: swirl 5s linear forwards; }  # Increased duration to 5s
    @keyframes swirl { 0% { transform: rotate(0deg) scale(1); opacity: 1; } 100% { transform: rotate(720deg) scale(0); opacity: 0; } }
    .overlay { position: fixed; bottom: 20px; right: 20px; background-color: rgba(0, 0, 0, 0.8); padding: 10px; border-radius: 10px; box-shadow: 0 0 20px #00ffff; z-index: 1000; color: #ffffff; text-align: center; transition: opacity 0.3s; width: 300px; }
    .overlay button { background-color: #1a1a3a; color: #00ffff; border: 1px solid #00ffff; box-shadow: 0 0 5px #00ffff; padding: 5px 10px; cursor: pointer; }
    .log-container { width: 100%; height: 200px; overflow-y: auto; background-color: #1a1a3a; padding: 10px; border: 1px solid #00ffff; }
    .log-container::-webkit-scrollbar { width: 8px; }
    .log-container::-webkit-scrollbar-thumb { background-color: #00ffff; border-radius: 4px; }
    .queue-container { width: 100%; margin-bottom: 20px; }
    .status-row { display: flex; justify-content: space-between; margin-bottom: 20px; }
    .charts-row { display: flex; justify-content: space-between; margin-top: 20px; }
    .chart-container { flex: 1; margin: 0 10px; height: 300px; }
    .tour-overlay { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.8); padding: 20px; border-radius: 10px; box-shadow: 0 0 20px #00ffff; z-index: 1000; color: #ffffff; text-align: center; transition: opacity 0.3s; width: 400px; }
    .avatar { font-size: 50px; margin-bottom: 10px; }
    @media (max-width: 768px) { .status-row { flex-direction: column; } .charts-row { flex-direction: column; } .chart-container { height: auto; margin-bottom: 20px; } .tour-overlay { width: 80%; } .overlay { width: 90%; bottom: 10px; right: 10px; } }
    </style>
    <script>
    function autoScroll() {
        var container = document.getElementById('log-scroll');
        if (container) {
            setTimeout(() => {
                container.scrollTop = container.scrollHeight;
            }, 100); // Delay to ensure DOM update
        }
    }
    </script>
""", unsafe_allow_html=True)

# Disclaimer at the top
st.markdown("<h3 style='color: #00ffff; text-align: center;'>Disclaimer: Simulation adjusted for 25 minutes; all proportions scaled to 10 seconds per block emission.</h3>", unsafe_allow_html=True)

# Initialize session state from zero
if 'running' not in st.session_state:
    st.session_state.running = False
if 'speed' not in st.session_state:
    st.session_state.speed = 1
if 'block_number' not in st.session_state:
    st.session_state.block_number = 0
if 'current_reward' not in st.session_state:
    st.session_state.current_reward = 25.0
if 'circulating_supply' not in st.session_state:
    st.session_state.circulating_supply = 0.0
if 'burned_coins' not in st.session_state:
    st.session_state.burned_coins = 0.0
if 'treasury_coins' not in st.session_state:
    st.session_state.treasury_coins = 0.0
if 'current_era' not in st.session_state:
    st.session_state.current_era = 1
if 'blocks_in_current_era' not in st.session_state:
    st.session_state.blocks_in_current_era = 0
if 'halving_interval' not in st.session_state:
    st.session_state.halving_interval = 20  # Scaled for demo; original 210,000
if 'era_durations_blocks' not in st.session_state:
    st.session_state.era_durations_blocks = [40, 30] * 5  # Scaled for demo; original ~210,000
if 'total_blocks_in_era' not in st.session_state:
    st.session_state.total_blocks_in_era = st.session_state.era_durations_blocks[0]
if 'active_wallets_pct' not in st.session_state:
    st.session_state.active_wallets_pct = 100
if 'dormant_wallets_pct' not in st.session_state:
    st.session_state.dormant_wallets_pct = 0
if 'frozen_wallets_pct' not in st.session_state:
    st.session_state.frozen_wallets_pct = 0
if 'erased_wallets_pct' not in st.session_state:
    st.session_state.erased_wallets_pct = 0
if 'logs' not in st.session_state:
    st.session_state.logs = ["[INIT] Protocol initialized: Fully decentralized, validator-free simulation starting from genesis."]
if 'reward_history' not in st.session_state:
    st.session_state.reward_history = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'quantum_triggered' not in st.session_state:
    st.session_state.quantum_triggered = False
if 'overlay_message' not in st.session_state:
    st.session_state.overlay_message = None
if 'filter_type' not in st.session_state:
    st.session_state.filter_type = 'All'
if 'cosmic_labs_balance' not in st.session_state:
    st.session_state.cosmic_labs_balance = 0.0
if 'active_miners_balance' not in st.session_state:
    st.session_state.active_miners_balance = 0.0
if 'stakers_balance' not in st.session_state:
    st.session_state.stakers_balance = 0.0
if 'failure_rate' not in st.session_state:
    st.session_state.failure_rate = 0.3
if 'tour_step' not in st.session_state:
    st.session_state.tour_step = 0  # For guided tour
if 'tour_active' not in st.session_state:
    st.session_state.tour_active = False  # Start with tour off; button to start

# Button to start/restart tour
if st.button("Start Guided Tour", key="start_tour_main"):
    st.session_state.tour_active = True
    st.session_state.tour_step = 0
    st.rerun()

# Guided Tour Mode
tour_steps = [
    "🌌 Cosmic Guide: Welcome to the Cosmic Chain Protocol simulation! This demo showcases the protocol's mechanics. Logic: Simulates block emission every 10 seconds to demonstrate consensus and burns. Mainnet: Real blocks emit every 10 minutes. Reason: Accelerates cosmic cycles for demo.",
    "🌌 Cosmic Guide: The 'Start Simulation' button begins the block emission process. 'Stop' pauses it. 'Fast Forward' speeds up the process. 'Progress' tracks the 25-minute demo. Logic: Controls simulation flow. Mainnet: Runs continuously. Reason: Mimics universe's perpetual motion.",
    "🌌 Cosmic Guide: The 'Blockchain & Orbit Queue' shows pending blocks as orbs. Numbers indicate validation order. Logic: Random queue ensures fairness. Mainnet: Real nodes submit blocks. Reason: Prevents spam, aligns with entropy.",
    "🌌 Cosmic Guide: Micro PoW and PoS validate blocks. Failure (30% rate here for demo) triggers a Blackhole Burn. Logic: Dual consensus without validators. Mainnet: Failures based on node performance. Reason: Discourages low-effort mining.",
    "🌌 Cosmic Guide: Live Metrics & Protocol Stats show real-time balances, rewards, and supply. Logic: Tracks economic state. Mainnet: On-chain data. Reason: Transparency for self-balancing.",
    "🌌 Cosmic Guide: Charts display supply (pie), rewards (line), and wallet lifecycle (bar). Logic: Visualizes entropy and resets. Mainnet: Based on live activity. Reason: Illustrates dynamic scarcity.",
    "🌌 Cosmic Guide: Tour complete! Start the simulation to explore. Logs auto-scroll for latest events."
]

if st.session_state.tour_active and st.session_state.tour_step < len(tour_steps):
    st.markdown(f"""
        <div class="tour-overlay">
            <div class="avatar">🌌</div>
            <p>{tour_steps[st.session_state.tour_step]}</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])  # Left-aligned
    with col1:
        if st.button("Back", key="back_tour") and st.session_state.tour_step > 0:
            st.session_state.tour_step -= 1
            st.rerun()
        if st.button("Start Guided Tour", key="start_tour_restart"):  # Allow restart
            st.session_state.tour_active = True
            st.session_state.tour_step = 0
            st.rerun()
    with col2:
        if st.button("Next", key="next_tour"):
            st.session_state.tour_step += 1
            if st.session_state.tour_step >= len(tour_steps):
                st.session_state.tour_active = False
            st.rerun()
    with col3:
        if st.button("Skip Tour", key="skip_tour"):
            st.session_state.tour_active = False
            st.session_state.tour_step = len(tour_steps)
            st.rerun()

# Header
st.title("Cosmic Chain Protocol – Live Simulation")

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Start Simulation 🔵", key="start_sim"):
        st.session_state.running = True
        st.session_state.start_time = time.time()
with col2:
    if st.button("Stop Simulation 🔴", key="stop_sim"):
        st.session_state.running = False
with col3:
    speed = st.selectbox("Fast Forward", ["x1", "x2", "x5", "x10"], index=0, key="speed_select", help="Accelerate simulation speed to see events like halvings and resets faster.")
    st.session_state.speed = int(speed[1:])
with col4:
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        progress = min(elapsed / (25 * 60), 1.0)  # 25 min progress
        st.progress(progress)
        st.caption(f"Progress: {int(progress * 100)}%")

# Full-width Blockchain & Orbit Queue
st.subheader("Blockchain & Orbit Queue")
queue_html = '<div class="queue-container">' + ''.join([f'<div class="orb" data-block="{st.session_state.block_number + i + 1}"></div>' for i in range(5)]) + '</div>'
st.markdown(queue_html, unsafe_allow_html=True)

# Micro PoW, PoS, Validation Status, Blackhole Burn in a row
status_row = st.columns(4)
pow_status = status_row[0].empty()
pos_status = status_row[1].empty()
block_status = status_row[2].empty()
blackhole_status = status_row[3].empty()

# Live Metrics & Protocol Stats in two rows
st.subheader("Live Metrics & Protocol Stats")
# Row 1: Wallet balances and current reward
row1 = st.columns(5)
row1[0].markdown('<div class="metric-box">Cosmic Labs: {:.0f} COS</div>'.format(st.session_state.cosmic_labs_balance), unsafe_allow_html=True)
row1[1].markdown('<div class="metric-box">Active Miners: {:.0f} COS</div>'.format(st.session_state.active_miners_balance), unsafe_allow_html=True)
row1[2].markdown('<div class="metric-box">Stakers: {:.0f} COS</div>'.format(st.session_state.stakers_balance), unsafe_allow_html=True)
row1[3].markdown('<div class="metric-box">Current Reward: {:.2f} COS/block</div>'.format(st.session_state.current_reward), unsafe_allow_html=True)
row1[4].markdown('<div class="metric-box">Current ERA: {}</div>'.format(st.session_state.current_era), unsafe_allow_html=True)

# Row 2: Countdowns and supply metrics
row2 = st.columns(5)
row2[0].markdown('<div class="metric-box">Halving Countdown: {} blocks</div>'.format(st.session_state.halving_interval - (st.session_state.block_number % st.session_state.halving_interval)), unsafe_allow_html=True)
row2[1].markdown('<div class="metric-box">Reset Trigger Countdown: {} blocks</div>'.format(st.session_state.total_blocks_in_era - st.session_state.blocks_in_current_era), unsafe_allow_html=True)
row2[2].markdown('<div class="metric-box">Days Left in ERA: {}</div>'.format((st.session_state.total_blocks_in_era - st.session_state.blocks_in_current_era) // 144), unsafe_allow_html=True)
row2[3].markdown('<div class="metric-box">Total Supply: {:.0f} COS (Ref: 10M)</div>'.format(st.session_state.circulating_supply + st.session_state.burned_coins + st.session_state.treasury_coins), unsafe_allow_html=True)
row2[4].markdown('<div class="metric-box">Circulating Supply: {:.0f} COS</div>'.format(st.session_state.circulating_supply), unsafe_allow_html=True)

# Charts below metrics, in a single row
if st.session_state.block_number > 0:
    charts_row = st.columns(3)
    with charts_row[0]:
        fig, ax = plt.subplots(figsize=(4, 3))
        labels = ['Circulating', 'Burned', 'Treasury']
        sizes = [st.session_state.circulating_supply, st.session_state.burned_coins, st.session_state.treasury_coins]
        if sum(sizes) > 0:
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#00ffff', '#ff8800', '#ff00ff'])
            ax.set_title('Supply Distribution', color='#ffffff')
            fig.patch.set_facecolor('#0a0a1f')
            ax.set_facecolor('#0a0a1f')
            plt.setp(ax.texts, color='#ffffff')
            st.pyplot(fig)
        else:
            st.write("No supply data yet.")
    with charts_row[1]:
        if st.session_state.reward_history:
            reward_df = pd.DataFrame(st.session_state.reward_history, columns=['Block', 'Reward'])
            st.line_chart(reward_df.set_index('Block'))
    with charts_row[2]:
        lifecycle_data = pd.DataFrame({
            'Status': ['Active', 'Dormant', 'Frozen', 'Erased'],
            'Percentage': [st.session_state.active_wallets_pct, st.session_state.dormant_wallets_pct, 
                           st.session_state.frozen_wallets_pct, st.session_state.erased_wallets_pct]
        })
        st.bar_chart(lifecycle_data.set_index('Status'))

# Bottom: Full-width auto-scrolling Logs
st.subheader("Protocol Logs & Insights")
filter_type = st.selectbox("Filter by Event Type", ['All', 'Pass', 'Fail', 'Burn', 'Reset', 'Quantum'], key="filter_select", help="Filter logs to show specific event types.")
st.session_state.filter_type = filter_type
log_container = st.empty()
def update_logs():
    filtered_logs = [log for log in st.session_state.logs if filter_type == 'All' or filter_type.lower() in log.lower()]
    log_html = '<div class="log-container" id="log-scroll">'
    for log in filtered_logs:
        if 'pass' in log.lower():
            log_html += f'<p class="log-entry-pass" title="Successful block validation and addition to chain.">{log}</p>'
        elif 'fail' in log.lower():
            log_html += f'<p class="log-entry-fail" title="Block failed PoW or PoS; triggers burn penalty.">{log}</p>'
        elif 'burn' in log.lower():
            log_html += f'<p class="log-entry-burn" title="Coins burned due to failure or inactivity, enforcing entropy.">{log}</p>'
        elif 'reset' in log.lower():
            log_html += f'<p class="log-entry-reset" title="Protocol reset: Rewards renewed to 25 COS at ERA end if <=1.">{log}</p>'
        elif 'quantum' in log.lower():
            log_html += f'<p class="log-entry-quantum" title="Quantum Leap Era triggered: Migrating to post-quantum crypto.">{log}</p>'
        else:
            log_html += f'<p>{log}</p>'
    log_html += '</div><script>autoScroll();</script>'
    log_container.markdown(log_html, unsafe_allow_html=True)
update_logs()

# Overlay for milestones
if st.session_state.overlay_message:
    st.markdown(f"""
        <div class="overlay">
            <h2>{st.session_state.overlay_message}</h2>
            <button onclick="this.parentElement.style.display='none';">Close</button>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Close", key="close_overlay"):  # Unique key
        st.session_state.overlay_message = None
        st.rerun()

# Simulation logic
def mine_block():
    st.session_state.block_number += 1
    st.session_state.blocks_in_current_era += 1
    
    # Orbital delay animation (simulated)
    time.sleep(1 / st.session_state.speed)
    
    # Micro PoW
    pow_status.markdown("Micro PoW: Validating... 🔄")
    time.sleep(1 / st.session_state.speed)
    
    # Micro PoS
    pos_status.markdown("Micro PoS: Validating... 🔄")
    time.sleep(1 / st.session_state.speed)
    
    # Validation - using fixed failure rate for simulation
    if random.random() < st.session_state.failure_rate:
        burn = random.uniform(5, 10)
        st.session_state.burned_coins += burn * 0.5  # 50% burned
        st.session_state.cosmic_labs_balance += burn * 0.25  # 25% to Cosmic Labs
        st.session_state.stakers_balance += burn * 0.25  # 25% to Stakers
        st.session_state.logs.append(f"[FAIL] Block #{st.session_state.block_number} failed validation. Blackhole Burn: {burn:.2f} COS")
        block_status.markdown(f"Block #{st.session_state.block_number}: FAIL ❌")
        blackhole_status.markdown('<div class="blackhole" id="blackhole-animation">🕳️ Burned {burn:.2f} COS</div>', unsafe_allow_html=True)
        time.sleep(5)  # Ensure 5s visibility
        blackhole_status.empty()  # Clear after animation
        return 0.0, burn
    
    # Success - Full reward to miners
    reward = st.session_state.current_reward
    st.session_state.circulating_supply += reward
    st.session_state.active_miners_balance += reward  # 100% to miners
    st.session_state.logs.append(f"[PASS] Block #{st.session_state.block_number} mined successfully. Reward: {reward:.2f} COS")
    block_status.markdown(f"Block #{st.session_state.block_number}: PASS ✅ Reward: {reward:.2f}")
    st.session_state.reward_history.append([st.session_state.block_number, reward])
    
    # Inactivity burn
    if st.session_state.block_number > 10 and random.random() < 0.2:
        inactivity_burn = st.session_state.circulating_supply * 0.002 * (st.session_state.dormant_wallets_pct / 100)
        st.session_state.burned_coins += inactivity_burn * 0.5  # 50% burned
        st.session_state.cosmic_labs_balance += inactivity_burn * 0.25  # 25% to Cosmic Labs
        st.session_state.stakers_balance += inactivity_burn * 0.25  # 25% to Stakers
        st.session_state.circulating_supply -= inactivity_burn
        st.session_state.logs.append(f"[BURN] Wallet inactivity decay: {inactivity_burn:.2f} COS")
    
    # Wallet lifecycle shift
    shift = random.randint(-2, 2)
    st.session_state.active_wallets_pct = max(0, min(100, st.session_state.active_wallets_pct + shift))
    st.session_state.dormant_wallets_pct = max(0, min(100 - st.session_state.active_wallets_pct, st.session_state.dormant_wallets_pct - shift // 2))
    st.session_state.frozen_wallets_pct = max(0, min(100 - st.session_state.active_wallets_pct - st.session_state.dormant_wallets_pct, st.session_state.frozen_wallets_pct))
    st.session_state.erased_wallets_pct = 100 - (st.session_state.active_wallets_pct + st.session_state.dormant_wallets_pct + st.session_state.frozen_wallets_pct)
    
    # Halving
    if st.session_state.block_number % st.session_state.halving_interval == 0:
        st.session_state.current_reward /= 2
        st.session_state.logs.append(f"[HALVING] Reward halved to {st.session_state.current_reward:.2f} COS")
    
    # ERA end and reset
    if st.session_state.blocks_in_current_era >= st.session_state.total_blocks_in_era:
        if st.session_state.current_reward <= 1.0:
            st.session_state.logs.append(f"[RESET] Protocol Reset: Reward <=1 at ERA end. Resetting to 25 COS.")
            st.session_state.overlay_message = "Cosmic Reboot: Renewing incentives like a universe rebirth!"
            st.session_state.current_reward = 25.0
        st.session_state.current_era += 1
        st.session_state.blocks_in_current_era = 0
        era_index = min(st.session_state.current_era - 1, len(st.session_state.era_durations_blocks) - 1)
        st.session_state.total_blocks_in_era = st.session_state.era_durations_blocks[era_index]
    
    # Quantum trigger
    if st.session_state.block_number == 100 and not st.session_state.quantum_triggered:
        st.session_state.quantum_triggered = True
        st.session_state.logs.append(f"[QUANTUM] Quantum Readiness Triggered: Migrating to QLE.")
        st.session_state.overlay_message = "Quantum Leap Era: Activating post-quantum migration tools!"
    
    # Update logs
    update_logs()

# Run simulation if active
if st.session_state.running:
    mine_block()
    time.sleep(10 / st.session_state.speed)  # Block every 10 sec / speed
    st.rerun()