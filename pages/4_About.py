"""About the site and how picks are measured."""

import streamlit as st

import site_common as sc

sc.setup("About")
st.title("About")

st.markdown(f"""
I'm {sc.OWNER}, a sophomore studying finance at Baruch College's Zicklin School of Business.
I'm currently a Private Equity Intern and I'm especially interested in fixed income and credit.

**Also see:** my [Credit & Rates Dashboard]({sc.DASHBOARD_URL}) · [LinkedIn]({sc.LINKEDIN_URL})

### How picks are measured

- **Entry price** is the first market close on or after the day I publish a pick, so I can't choose a convenient price after the fact.
- **Return** is the change from the entry price to the latest close, or to the exit price for closed picks. Short picks gain when the price falls.
- **Vs. S&P 500** compares each pick with the S&P 500 (SPY, including dividends) over exactly the same dates.
- Prices are adjusted for splits and dividends, and come from Yahoo Finance.
- Every pick is timestamped in a public GitHub history, and no pick is ever removed.
- Credit ideas are published with the yield or spread at the time, but aren't tracked for P&L.

### Disclaimer

{sc.DISCLAIMER}
""")
