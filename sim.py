import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Matplotlib 설정
plt.rcParams['axes.unicode_minus'] = False  # Use ASCII minus instead of Unicode minus

# Streamlit page setup
st.title("Investment Simulation Graph (Cumulative Change, Log Scale)")
st.write("Adjust the input values and press 'Rerun' to re-execute the simulation.")

# Input values
success_prob = st.slider("Success Probability (0-1)", 0.0, 1.0, 0.5, 0.01)
success_multiplier = st.slider("Success Multiplier (e.g., 1.3 = 30% profit)", 1.0, 10.0, 1.3, 0.01)
failure_multiplier = st.slider("Failure Multiplier (e.g., 0.7 = -30% loss)", 0.0, 1.0, 0.7, 0.01)
leverage = st.slider("Leverage Ratio (0-1)", 0.0, 1.0, 0.1, 0.01)

# Initial investment and number of trials
initial_investment = 1  # Starting with 1
trials = 10000  # 10,000 simulations

# Simulation function
def run_simulation(prob, success_mult, failure_mult, lev, trials, initial):
    balance = [initial]  # Record of balance changes
    current_balance = initial
    
    # Run simulation
    for _ in range(trials):
        # Investment amount (with leverage)
        investment = current_balance * lev
        
        # Random success/failure
        if np.random.random() < prob:
            # Success case
            profit = investment * (success_mult - 1)
            current_balance += profit
        else:
            # Failure case
            loss = investment * (1 - failure_mult)
            current_balance -= loss
            
        # Prevent negative balance
        current_balance = max(0, current_balance)
        balance.append(current_balance)
    
    return balance

# State management: Check if button is clicked
if 'results' not in st.session_state:
    st.session_state.results = run_simulation(success_prob, success_multiplier, failure_multiplier, leverage, trials, initial_investment)

# Rerun button
if st.button("Rerun"):
    st.session_state.results = run_simulation(success_prob, success_multiplier, failure_multiplier, leverage, trials, initial_investment)

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.plot(st.session_state.results, label="Balance Change (Cumulative)")
plt.axhline(y=initial_investment, color='r', linestyle='--', label="Initial Investment")
plt.yscale('log')  # Set y-axis to log scale
plt.title(f"10,000 Investment Simulations (Log Scale)\nSuccess Prob: {success_prob}, Success Mult: {success_multiplier}, Failure Mult: {failure_multiplier}, Leverage: {leverage}")
plt.xlabel("Number of Trials")
plt.ylabel("Cumulative Balance (Log Scale)")
plt.legend()
plt.grid(True, which="both", ls="--")  # Grid for log scale

# Display graph in Streamlit
st.pyplot(plt)

# Result summary
st.write(f"Initial Investment: {initial_investment}")
st.write(f"Final Balance: {st.session_state.results[-1]:.2f}")
st.write(f"Cumulative Return: {((st.session_state.results[-1] - initial_investment) / initial_investment * 100):.2f}%")
