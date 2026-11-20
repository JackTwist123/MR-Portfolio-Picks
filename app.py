"""Home page: the scoreboard for every stock pick."""

import pandas as pd
import streamlit as st

import site_common as sc

sc.setup("Scoreboard")

st.title(sc.SITE_TITLE)
st.write(
    "My stock picks and credit ideas, each published with a dated thesis. "
    "Open picks update with live prices, and every return is compared with the S&P 500 over the same dates. "
    "Every pick stays on the record, winners and losers."
)

scored, _ = sc.scored_stock_picks()

if not scored:
    st.info("No stock picks published yet.")
    sc.footer()
    st.stop()

stats = sc.lib.summary_stats(scored)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Stock picks", stats["count"])
c2.metric("Hit rate", sc.pct(stats["hit_rate"], signed=False), help="Share of picks with a positive return")
c3.metric("Average return", sc.pct(stats["avg_return"]))
c4.metric("Average vs. S&P 500", sc.pct(stats["avg_vs_spy"]), help="Pick return minus the S&P 500's return over the same dates")


def table(rows):
    df = pd.DataFrame([{
        "Ticker": r["ticker"],
        "Company": r["name"],
        "Call": r["direction"].title(),
        "Entered": r["entered"],
        "Entry": sc.money(r["entry"]),
        "Current / exit": sc.money(r["last"]),
        "Return": sc.pct(r["return"]),
        "S&P 500": sc.pct(r["spy_return"]),
        "Vs. S&P": sc.pct(r["vs_spy"]),
        "Target": sc.money(r["target"]) if r["target"] else "–",
        "Stop": sc.money(r["stop"]) if r["stop"] else "–",
    } for r in sorted(rows, key=lambda r: r["entered"], reverse=True)])
    st.dataframe(df, hide_index=True, use_container_width=True)


open_rows = [r for r in scored if r["status"] != "closed"]
closed_rows = [r for r in scored if r["status"] == "closed"]

st.subheader(f"Open picks ({len(open_rows)})")
if open_rows:
    table(open_rows)
else:
    st.caption("None right now.")

st.subheader(f"Closed picks ({len(closed_rows)})")
if closed_rows:
    table(closed_rows)
else:
    st.caption("None yet.")

st.caption("Read the full thesis for any pick on the Stock Picks page. Credit ideas are on their own page.")
sc.footer()
