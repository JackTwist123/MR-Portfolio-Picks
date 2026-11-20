"""One page per stock pick: key numbers, a price chart since entry, and the full thesis."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import site_common as sc

sc.setup("Stock Picks")
st.title("Stock Picks")

scored, prices = sc.scored_stock_picks()
if not scored:
    st.info("No stock picks published yet.")
    sc.footer()
    st.stop()

picks = {p["slug"]: p for p in sc.stock_picks()}
ordered = sorted(scored, key=lambda r: r["entered"], reverse=True)
labels = {
    r["slug"]: f"{r['ticker']} · {r['direction'].title()} · {r['entered']:%b %d, %Y}"
    + (" (closed)" if r["status"] == "closed" else "")
    for r in ordered
}
slug = st.selectbox("Choose a pick", [r["slug"] for r in ordered], format_func=labels.get)
r = next(x for x in ordered if x["slug"] == slug)
pick = picks[slug]

st.header(f"{r['direction'].title()} {r['ticker']}: {r['name']}")
if pick.get("headline"):
    st.markdown(f"**{pick['headline']}**")
st.caption(
    f"Entered {r['entered']:%B %d, %Y} · Published {r['published']:%B %d, %Y} · Status: {r['status'].title()}"
    + (f" · Closed {r['closed']:%B %d, %Y}" if r["closed"] else "")
    + (f" · Horizon: {pick['horizon']}" if pick.get("horizon") else "")
)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Entry", sc.money(r["entry"]))
c2.metric("Exit" if r["status"] == "closed" else "Current", sc.money(r["last"]))
c3.metric("Return", sc.pct(r["return"]))
c4.metric("Vs. S&P 500", sc.pct(r["vs_spy"]))
c5.metric("Target", sc.money(r["target"]) if r["target"] else "–")
c6.metric("Stop", sc.money(r["stop"]) if r["stop"] else "–")
if r["backfilled"]:
    st.info(
        f"Added after the fact: this position was entered on {r['entered']:%B %d, %Y}"
        + (f" and closed on {r['closed']:%B %d, %Y}" if r["closed"] else "")
        + f", before it was published here on {r['published']:%B %d, %Y}."
    )
if r["note"]:
    st.warning(r["note"])

# Price chart from entry to today (or the close date)
if prices is not None and r["ticker"] in prices.columns and r["entry_date"]:
    s = prices[r["ticker"]].dropna()
    s = s[(s.index >= pd.Timestamp(r["entry_date"])) & (s.index <= pd.Timestamp(r["last_date"]))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=s.index, y=s.values, name=r["ticker"], line=dict(width=2.5)))
    fig.add_hline(y=r["entry"], line_dash="dot", line_color="gray", annotation_text="Entry")
    if r["target"]:
        fig.add_hline(y=float(r["target"]), line_dash="dash", line_color="green", annotation_text="Target")
    if r["stop"]:
        fig.add_hline(y=float(r["stop"]), line_dash="dash", line_color="red", annotation_text="Stop")
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10), yaxis_title="Price ($)",
                      showlegend=False, title=f"{r['ticker']} since entry")
    st.plotly_chart(fig, use_container_width=True)

pitch, closing = sc.lib.split_closing_note(pick["body"])
if closing:
    st.subheader("Closing note")
    st.markdown(closing)
    st.divider()
st.markdown(pitch)

sc.footer()
