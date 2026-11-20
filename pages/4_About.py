"""About the site and how picks are measured."""

import streamlit as st

import site_common as sc

sc.setup("About")
st.title("About")

st.markdown(f"""
I'm {sc.OWNER}, a sophomore studying finance at Baruch College's Zicklin School of Business.
I'm currently a Private Equity Intern, and I'm especially interested in fixed income and credit.

**Also see:** my [Credit & Rates Dashboard]({sc.DASHBOARD_URL}) · [LinkedIn]({sc.LINKEDIN_URL})

### How picks are measured

- **Entry and exit** are my actual trade dates and prices. Where I don't list a price, the site uses that day's closing price.
- **Open picks** update with live market prices.
- **Return** is the change from entry to the latest close, or to the exit for closed picks. Short picks gain when the price falls.
- **Vs. S&P 500** compares each pick with the S&P 500 (SPY, including dividends) over exactly the same dates.
- Prices are adjusted for splits and dividends, and come from Yahoo Finance.
- Winners and losers both stay on the record. No pick is removed.
- Credit ideas are published with the yield or spread at the time, but aren't tracked for P&L.

### Disclaimer

{sc.DISCLAIMER}
""")
