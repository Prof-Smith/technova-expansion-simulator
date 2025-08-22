
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from math import pi

st.set_page_config(layout="wide")

# Define countries and factors for comparative advantage
demo_countries = ['Brazil', 'Germany', 'India', 'Mexico', 'Vietnam', 'South Korea']
factors = ['Labor Productivity', 'Capital Availability', 'Technology Infrastructure']

# Tabs for navigation
tab1, tab2, tab3, tab4 = st.tabs(["Simulator", "Scenarios", "Comparative Advantage", "Educational Resources"])

with tab1:
    st.header("Interactive Cost and Profit Simulator")
    exchange_rates = {'Brazil': 5.2, 'Germany': 0.9, 'India': 83.0}
    local_costs = {'Brazil': 100.0, 'Germany': 75.0, 'India': 6000.0}
    selling_prices = {'Brazil': 150.0, 'Germany': 130.0, 'India': 11000.0}

    st.sidebar.header("Adjust Exchange Rates")
    exchange_rates['Brazil'] = st.sidebar.slider("Brazil (BRL/USD)", 4.5, 6.0, 5.2)
    exchange_rates['Germany'] = st.sidebar.slider("Germany (EUR/USD)", 0.8, 1.1, 0.9)
    exchange_rates['India'] = st.sidebar.slider("India (INR/USD)", 75.0, 90.0, 83.0)

    usd_costs = {c: local_costs[c] / exchange_rates[c] for c in exchange_rates}
    usd_prices = {c: selling_prices[c] / exchange_rates[c] for c in exchange_rates}
    usd_profits = {c: usd_prices[c] - usd_costs[c] for c in exchange_rates}

    cost_df = pd.DataFrame({
        'Country': list(exchange_rates.keys()),
        'Local Cost': [local_costs[c] for c in exchange_rates],
        'Selling Price': [selling_prices[c] for c in exchange_rates],
        'Exchange Rate': [exchange_rates[c] for c in exchange_rates],
        'USD Cost': [usd_costs[c] for c in exchange_rates],
        'USD Price': [usd_prices[c] for c in exchange_rates],
        'USD Profit': [usd_profits[c] for c in exchange_rates]
    })

    st.subheader("Comparative Cost and Profit Analysis")
    st.dataframe(cost_df)

    fig1, ax1 = plt.subplots()
    sns.barplot(x='Country', y='USD Profit', data=cost_df, palette='viridis', ax=ax1)
    ax1.set_title('Estimated Profit per Unit (USD)')
    ax1.set_ylabel('Profit in USD')
    st.pyplot(fig1)

with tab2:
    st.header("Scenario-Based Profitability Analysis")
    scenarios = {
        'Best Case': {
            'exchange_rates': {'Brazil': 5.0, 'Germany': 0.85, 'India': 80.0},
            'local_costs': {'Brazil': 95.0, 'Germany': 70.0, 'India': 5800.0},
            'selling_prices': {'Brazil': 160.0, 'Germany': 140.0, 'India': 11500.0}
        },
        'Expected Case': {
            'exchange_rates': {'Brazil': 5.2, 'Germany': 0.9, 'India': 83.0},
            'local_costs': {'Brazil': 100.0, 'Germany': 75.0, 'India': 6000.0},
            'selling_prices': {'Brazil': 150.0, 'Germany': 130.0, 'India': 11000.0}
        },
        'Worst Case': {
            'exchange_rates': {'Brazil': 5.5, 'Germany': 0.95, 'India': 87.0},
            'local_costs': {'Brazil': 110.0, 'Germany': 80.0, 'India': 6200.0},
            'selling_prices': {'Brazil': 140.0, 'Germany': 120.0, 'India': 10500.0}
        }
    }

    scenario_data = []
    for scenario, values in scenarios.items():
        for country in values['exchange_rates'].keys():
            usd_cost = values['local_costs'][country] / values['exchange_rates'][country]
            usd_price = values['selling_prices'][country] / values['exchange_rates'][country]
            usd_profit = usd_price - usd_cost
            scenario_data.append({
                'Scenario': scenario,
                'Country': country,
                'USD Cost': round(usd_cost, 2),
                'USD Price': round(usd_price, 2),
                'USD Profit': round(usd_profit, 2)
            })

    scenario_df = pd.DataFrame(scenario_data)
    st.dataframe(scenario_df)

    fig2, ax2 = plt.subplots()
    sns.barplot(x='Country', y='USD Profit', hue='Scenario', data=scenario_df, ax=ax2)
    ax2.set_title('Profitability Across Scenarios')
    ax2.set_ylabel('Profit in USD')
    st.pyplot(fig2)

with tab3:
    st.header("Comparative Advantage Analysis")
    st.markdown("### Adjust Factor Scores (1-10)")
    scores = {}
    for country in demo_countries:
        with st.sidebar.expander(f"{country} Factors"):
            scores[country] = [
                st.slider(f"{factor} ({country})", 1, 10, 5) for factor in factors
            ]

    df = pd.DataFrame(scores, index=factors).T

    def make_radar_chart(data, title):
        labels = list(data.columns)
        num_vars = len(labels)
        angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
        angles += angles[:1]
        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        for i, row in data.iterrows():
            values = row.tolist()
            values += values[:1]
            ax.plot(angles, values, label=i)
            ax.fill(angles, values, alpha=0.1)
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids([a * 180/pi for a in angles[:-1]], labels)
        ax.set_ylim(0, 10)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.title(title)
        st.pyplot(fig)

    st.subheader("Comparative Advantage Radar Chart")
    make_radar_chart(df, "Factor-Based Comparative Advantage")

    st.markdown("### Country Strength Summaries")
    summaries = {
        "Brazil": "Strong in natural resources and a growing tech sector, but moderate in capital availability.",
        "Germany": "Highly developed infrastructure, strong capital markets, and advanced technology.",
        "India": "Large labor force and improving tech sector, but capital availability is still developing.",
        "Mexico": "Cost-effective labor and proximity to the U.S. market, with growing capital access.",
        "Vietnam": "Competitive labor costs and increasing investment in technology and infrastructure.",
        "South Korea": "High-tech infrastructure, strong R&D capabilities, and robust capital markets."
    }
    for country, summary in summaries.items():
        st.markdown(f"**{country}**: {summary}")

with tab4:
    st.header("Educational Resources")
    st.markdown("""
### Concept Guides
- **Comparative Advantage**: Learn how countries specialize based on resource endowments.
- **Exchange Rate Mechanics**: Understand bid/ask spreads, mid-rates, and currency impacts.
- **Globalization Process**: Explore the stages from domestic to multinational operations.

### Discussion Prompts
- How should TechNova hedge against currency risk?
- What ethical considerations arise when entering emerging markets?
- How do cultural differences impact financial decision-making?

### Suggested Readings
- *Fundamentals of Multinational Finance* by Eiteman et al. (Chapter 1)
- OECD and UNCTAD reports on international business trends
- Articles on foreign direct investment and global supply chains

### Activities
- **Simulation Challenge**: Act as TechNova’s executive board and make strategic decisions.
- **Sensitivity Analysis Lab**: Model how changes in costs or exchange rates affect profitability.
- **Strategic Memo**: Write a recommendation for TechNova’s expansion strategy.
""")
