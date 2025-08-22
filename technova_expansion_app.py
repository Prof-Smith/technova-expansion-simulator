
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data
exchange_rates = {'Brazil': 5.2, 'Germany': 0.9, 'India': 83.0}
local_costs = {'Brazil': 120.0, 'Germany': 85.0, 'India': 7000.0}

st.title("TechNova Inc. International Expansion Simulator")

st.markdown("""
### Instructions:
1. Use the sliders to adjust exchange rate assumptions.
2. View updated cost comparisons and risk assessments.
3. Discuss implications with your team.
""")

# Sidebar for exchange rate adjustments
st.sidebar.header("Adjust Exchange Rates")
exchange_rates['Brazil'] = st.sidebar.slider("Brazil (BRL/USD)", 4.5, 6.0, 5.2)
exchange_rates['Germany'] = st.sidebar.slider("Germany (EUR/USD)", 0.8, 1.1, 0.9)
exchange_rates['India'] = st.sidebar.slider("India (INR/USD)", 75.0, 90.0, 83.0)

# Calculate USD costs
usd_costs = {country: local_costs[country] / exchange_rates[country] for country in exchange_rates}
cost_df = pd.DataFrame({
    'Country': list(usd_costs.keys()),
    'Local Cost': [local_costs[c] for c in usd_costs],
    'Exchange Rate': [exchange_rates[c] for c in usd_costs],
    'USD Equivalent': list(usd_costs.values())
})
cost_df['5% Depreciation'] = cost_df['Local Cost'] / (cost_df['Exchange Rate'] * 1.05)
cost_df['5% Appreciation'] = cost_df['Local Cost'] / (cost_df['Exchange Rate'] * 0.95)

# Display cost table
st.subheader("Comparative Cost Analysis")
st.dataframe(cost_df)

# Bar chart
fig1, ax1 = plt.subplots()
ax1.bar(cost_df['Country'], cost_df['USD Equivalent'], color='skyblue')
ax1.set_title('USD Equivalent Manufacturing Costs')
ax1.set_ylabel('Cost in USD')
st.pyplot(fig1)

# Line chart
fig2, ax2 = plt.subplots()
for col in ['USD Equivalent', '5% Depreciation', '5% Appreciation']:
    ax2.plot(cost_df['Country'], cost_df[col], marker='o', label=col)
ax2.set_title('Currency Risk Sensitivity')
ax2.set_ylabel('Cost in USD')
ax2.legend()
st.pyplot(fig2)

# Risk matrix
risk_levels = {'Low': 1, 'Medium': 2, 'High': 3}
risk_matrix = pd.DataFrame({
    'Risk Factor': ['Political Risk', 'Exchange Rate Volatility', 'Supply Chain Disruption'],
    'Brazil': ['High', 'Medium', 'Medium'],
    'Germany': ['Low', 'Low', 'Low'],
    'India': ['Medium', 'High', 'High']
})
risk_numeric = risk_matrix.set_index('Risk Factor').replace(risk_levels)
fig3, ax3 = plt.subplots()
sns.heatmap(risk_numeric, annot=risk_matrix.set_index('Risk Factor'), fmt='', cmap='YlOrRd', cbar=False, ax=ax3)
ax3.set_title('Scenario-Based Risk Matrix')
st.pyplot(fig3)

st.markdown("""
### Discussion Prompts:
- Which country offers the best cost advantage?
- How do currency fluctuations impact decision-making?
- What risks should TechNova prioritize in its strategy?
""")
