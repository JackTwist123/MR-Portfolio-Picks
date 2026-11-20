"""Shared pieces for every page: settings, cached data loading, formatting."""

import datetime as dt

import streamlit as st

import picks_lib as lib

# ---- Edit these to personalize the site ----
OWNER = "Mukund Rao"
SITE_TITLE = "Mukund Rao | Stock & Credit Ideas"
DASHBOARD_URL = "https://credit-rates.streamlit.app/"
LINKEDIN_URL = "https://www.linkedin.com/in/mukund-rao-7a2428383/"
# ---------------------------------------------

DISCLAIMER = (
    "For educational purposes only. These are my personal views, not investment advice "
    "or a recommendation to buy or sell any security."
)


def setup(page_title: str) -> None:
    st.set_page_config(page_title=f"{page_title} | {OWNER}", page_icon="📈", layout="wide")


def stock_picks() -> list[dict]:
    return lib.load_picks(lib.STOCK_DIR)


def bond_ideas() -> list[dict]:
    return lib.load_picks(lib.BOND_DIR)


@st.cache_data(ttl=900, show_spinner="Loading prices...")
def prices_for(tickers: tuple[str, ...], start: dt.date):
    return lib.fetch_prices(list(tickers), start)


def scored_stock_picks() -> tuple[list[dict], object]:
    """Load stock picks, fetch prices once, and score every pick."""
    picks = stock_picks()
    if not picks:
        return [], None
    tickers = tuple(sorted({str(p["ticker"]).upper() for p in picks} | {lib.BENCHMARK}))
    start = min(lib.entry_date_of(p) for p in picks)
    try:
        prices = prices_for(tickers, start)
    except Exception as e:
        st.error(f"Couldn't load prices right now: {e}")
        return [dict(lib.score_stock_pick(p, _empty()), note="Prices unavailable") for p in picks], None
    return [lib.score_stock_pick(p, prices) for p in picks], prices


def _empty():
    import pandas as pd
    return pd.DataFrame()


def pct(x, signed=True):
    if x is None:
        return "–"
    return f"{x:+.1%}" if signed else f"{x:.1%}"


def money(x):
    return "–" if x is None else f"${x:,.2f}"


def footer():
    st.divider()
    st.caption(DISCLAIMER)
