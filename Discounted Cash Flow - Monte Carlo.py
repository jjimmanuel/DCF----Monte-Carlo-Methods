import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

years = ['2022A', '2023P', '2024P', '2025P', '2026P', '2027P', '2028P']
rev = pd.Series(index=years)
rev['2022A'] = 10.0

rev_growth = 0.1

ebitda_margin = 0.25
depr_percent = 0.05
nwc_percent = 0.2
capex_percent = depr_percent
tax_rate = 0.25
cost_of_capital = 0.10
terminal_growth = 0.01

iterations = 10000

def simulation():
    rev_growth_dist = np.random.normal(loc=0.1, scale=0.01, size=iterations)
    ebitda_margin_dist = np.random.normal(loc=0.25, scale=0.01, size=iterations)
    nwc_percent_dist = np.random.normal(loc=0.2, scale=0.01, size=iterations)

    output_distribution = []
    for i in range(iterations):
        for year in range(1, 7):
            rev[year] = rev[year - 1] * (1 + rev_growth_dist[0])
        ebitda = rev * ebitda_margin_dist[i]
        depreciation = (rev * depr_percent)
        ebit = ebitda - depreciation
        nwc = rev * nwc_percent_dist[i]
        change_in_nwc = nwc.shift(1) - nwc
        capex = -(rev * capex_percent)
        tax_payment = -ebit * tax_rate
        tax_payment = tax_payment.apply(lambda x: min(x, 0))
        fcf = ebit + depreciation + tax_payment + capex + change_in_nwc

        # Valuation
        terminal_value = (fcf[-1] * 1.02) / (cost_of_capital - 0.02)
        fcf[-1] += terminal_value
        discount_factors = [(1 / (1 + cost_of_capital)) ** i for i in range(1, 7)]
        dcf_value = sum(fcf[1:] * discount_factors)
        output_distribution.append(dcf_value)

    return output_distribution

plt.hist(simulation())
plt.show()

