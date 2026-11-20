"""Closed stock picks with their results and what I learned from each."""

import streamlit as st

import site_common as sc

sc.setup("Track Record")
st.title("Track Record")
st.write("Every closed pick, with the result and an honest look at what I got right and wrong.")

scored, _ = sc.scored_stock_picks()
picks = {p["slug"]: p for p in sc.stock_picks()}
closed = sorted([r for r in scored if r["status"] == "closed"], key=lambda r: r["closed"] or r["entered"], reverse=True)

if not closed:
    st.info("No closed picks yet. Open picks are on the Scoreboard.")
    sc.footer()
    st.stop()

stats = sc.lib.summary_stats(closed)
c1, c2, c3 = st.columns(3)
c1.metric("Closed picks", stats["count"])
c2.metric("Hit rate", sc.pct(stats["hit_rate"], signed=False))
c3.metric("Average vs. S&P 500", sc.pct(stats["avg_vs_spy"]))
st.caption(
    f"Based on {stats['count']} pick(s) so far. With a small sample, one or two results can swing the hit rate "
    "and averages a lot, so expect these numbers to settle as more picks are added over time."
)

for r in closed:
    st.subheader(f"{r['direction'].title()} {r['ticker']}: {sc.pct(r['return'])} (S&P 500 {sc.pct(r['spy_return'])})")
    dates = f"Entered {r['entered']:%b %d, %Y}" + (f" · Closed {r['closed']:%b %d, %Y}" if r["closed"] else "")
    st.caption(dates)
    _, note = sc.lib.split_closing_note(picks[r["slug"]]["body"])
    st.markdown(note or "_Closing note to come._")
    st.divider()

sc.footer()
