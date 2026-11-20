# MR Portfolio Picks

A public record of my stock picks and credit ideas. Every pick has a written thesis and its actual entry and exit, and open stock picks update live against the S&P 500. Winners and losers both stay on the record.

## What's on the site

| Page | What it shows |
| --- | --- |
| **Scoreboard** | Every stock pick with entry price, current or exit price, return, and return vs. the S&P 500, plus hit rate and averages |
| **Stock Picks** | The full thesis for each pick, with a price chart since entry and target and stop levels |
| **Credit Ideas** | Bond and credit views, dated with the yield or spread when published (not tracked for P&L) |
| **Track Record** | Closed picks, with what I got right and wrong on each |
| **About** | Background, methodology and disclaimer |

## How picks are measured

- **Entry and exit** are my actual trade dates and prices. If a price isn't listed, that day's close is used.
- **Return** runs from entry to the latest close for open picks, or to the exit for closed picks. Shorts gain when the price falls.
- **Vs. S&P 500** compares each pick with SPY over exactly the same dates.
- Market prices come from Yahoo Finance. Closed picks in stocks that no longer trade are scored from their recorded prices.
- Winners and losers both stay on the record.

## Each stock pitch covers

1. The call
2. Company overview
3. What the market is missing
4. Why now: catalysts
5. Valuation
6. Risks and what would make me wrong

## Adding a pick

Copy `picks/stocks/_TEMPLATE.md`, rename it (for example `fun-2026-10.md`), fill in the entry date and price, and commit. For a closed pick, set `status: closed` and add `exited` and `exit_price`. The site picks it up automatically.

## Project structure

```
app.py               Scoreboard (home page)
pages/               Stock Picks, Credit Ideas, Track Record, About
picks/stocks/        One Markdown file per stock pick
picks/bonds/         One Markdown file per credit idea
picks_lib.py         Reads pick files and calculates returns
site_common.py       Shared settings and helpers
.streamlit/          Site theme
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Built with Python, Streamlit, Plotly and yfinance.

---

*For educational purposes only. These are my personal views, not investment advice or a recommendation to buy or sell any security.*

**Mukund Rao** · BBA Finance, Baruch College
