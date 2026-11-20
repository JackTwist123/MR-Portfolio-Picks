"""
Core logic for the picks site: reads pick files and calculates returns.
Kept separate from the pages so it's easy to test and reuse.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).parent
STOCK_DIR = ROOT / "picks" / "stocks"
BOND_DIR = ROOT / "picks" / "bonds"
BENCHMARK = "SPY"  # S&P 500 ETF, used as the benchmark for every stock pick
CLOSING_HEADING = "## Closing note"


# ------------------------------------------------------------ reading files ---

def parse_pick_file(path: Path) -> dict:
    """Split a pick file into its header fields (between the --- lines) and its body text."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: file must start with a --- header block")
    _, header, body = text.split("---", 2)
    fields = yaml.safe_load(header) or {}
    fields["body"] = body.strip()
    fields["file"] = path.name
    fields["slug"] = path.stem
    return fields


def load_picks(folder: Path) -> list[dict]:
    """Load every pick file in a folder. Files starting with _ (like _TEMPLATE.md) are skipped."""
    if not folder.exists():
        return []
    picks = []
    for path in sorted(folder.glob("*.md")):
        if path.name.startswith("_"):
            continue
        picks.append(parse_pick_file(path))
    return picks


def to_date(value) -> dt.date | None:
    """Accept a date written as 2026-11-24 (YAML reads it as a date) or as text."""
    if value in (None, ""):
        return None
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value).strip())


def split_closing_note(body: str) -> tuple[str, str]:
    """Separate the pitch from the '## Closing note' section, if there is one."""
    if CLOSING_HEADING in body:
        pitch, note = body.split(CLOSING_HEADING, 1)
        return pitch.strip(), note.strip()
    return body, ""


# ---------------------------------------------------------------- prices ---

def fetch_prices(tickers: list[str], start: dt.date) -> pd.DataFrame:
    """Daily closing prices (adjusted for splits and dividends) from Yahoo Finance."""
    import yfinance as yf

    data = yf.download(
        tickers, start=start - dt.timedelta(days=7), auto_adjust=True, progress=False
    )
    closes = data["Close"]
    if isinstance(closes, pd.Series):  # a single ticker comes back as a Series
        closes = closes.to_frame(name=tickers[0])
    closes.index = pd.to_datetime(closes.index).tz_localize(None)
    return closes.dropna(how="all")


def close_on_or_after(prices: pd.Series, day: dt.date) -> tuple[dt.date, float] | None:
    """First available close on or after a date (handles weekends and holidays)."""
    s = prices.dropna()
    s = s[s.index >= pd.Timestamp(day)]
    if s.empty:
        return None
    return s.index[0].date(), float(s.iloc[0])


def close_on_or_before(prices: pd.Series, day: dt.date) -> tuple[dt.date, float] | None:
    """Last available close on or before a date."""
    s = prices.dropna()
    s = s[s.index <= pd.Timestamp(day)]
    if s.empty:
        return None
    return s.index[-1].date(), float(s.iloc[-1])


# --------------------------------------------------------------- returns ---

def score_stock_pick(pick: dict, prices: pd.DataFrame, today: dt.date | None = None) -> dict:
    """
    Work out a stock pick's entry, current/exit price and returns.

    - Entry = first close on or after the published date (or entry_price if you set one).
    - Exit  = close on the closed date for closed picks (or exit_price if set);
              otherwise the latest close.
    - Shorts gain when the price falls.
    - The S&P 500 (SPY) return is measured over exactly the same dates.
    """
    today = today or dt.date.today()
    ticker = str(pick["ticker"]).upper()
    direction = str(pick.get("direction", "long")).lower()
    status = str(pick.get("status", "open")).lower()
    published = to_date(pick["published"])
    closed = to_date(pick.get("closed")) if status == "closed" else None

    out = {
        "slug": pick["slug"],
        "ticker": ticker,
        "name": pick.get("name", ticker),
        "direction": direction,
        "status": status,
        "published": published,
        "closed": closed,
        "target": pick.get("target"),
        "stop": pick.get("stop"),
        "entry": None, "entry_date": None,
        "last": None, "last_date": None,
        "return": None, "spy_return": None, "vs_spy": None,
        "note": "",
    }

    if ticker not in prices.columns or BENCHMARK not in prices.columns:
        out["note"] = "No price data"
        return out

    px, spy = prices[ticker], prices[BENCHMARK]

    entry = close_on_or_after(px, published)
    if entry is None:
        out["note"] = "Waiting for first close after publishing"
        return out
    entry_date, entry_px = entry
    if pick.get("entry_price"):
        entry_px = float(pick["entry_price"])

    end_day = closed or today
    last = close_on_or_before(px, end_day)
    last_date, last_px = last
    if status == "closed" and pick.get("exit_price"):
        last_px = float(pick["exit_price"])

    spy_entry = close_on_or_after(spy, entry_date)
    spy_last = close_on_or_before(spy, last_date)

    raw = last_px / entry_px - 1
    ret = raw if direction == "long" else -raw
    spy_ret = spy_last[1] / spy_entry[1] - 1 if spy_entry and spy_last else None

    out.update({
        "entry": entry_px, "entry_date": entry_date,
        "last": last_px, "last_date": last_date,
        "return": ret,
        "spy_return": spy_ret,
        "vs_spy": ret - spy_ret if spy_ret is not None else None,
    })
    return out


def summary_stats(scored: list[dict]) -> dict:
    """Headline numbers for the scoreboard."""
    rows = [s for s in scored if s["return"] is not None]
    if not rows:
        return {"count": len(scored), "hit_rate": None, "avg_return": None, "avg_vs_spy": None}
    returns = [s["return"] for s in rows]
    vs = [s["vs_spy"] for s in rows if s["vs_spy"] is not None]
    return {
        "count": len(scored),
        "hit_rate": sum(r > 0 for r in returns) / len(returns),
        "avg_return": sum(returns) / len(returns),
        "avg_vs_spy": sum(vs) / len(vs) if vs else None,
    }
