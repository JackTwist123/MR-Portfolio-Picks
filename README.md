# Stock & Credit Ideas

A public record of my stock picks and credit ideas. Each pick is published with a dated thesis, and stock picks are tracked live against the S&P 500.

Built in Python with Streamlit, Plotly and Yahoo Finance data.

## How it works

- Every pick is a Markdown file in `picks/stocks/` or `picks/bonds/`, with the key facts at the top and the thesis below.
- The site reads the files, pulls prices, and calculates each stock pick's return from the first close after publishing, compared with the S&P 500 over the same dates.
- Git history timestamps every pick.

## Add a pick

Copy `picks/stocks/_TEMPLATE.md`, rename it, fill it in, and commit. The site updates on its own.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author

Mukund Rao, BBA Finance, Baruch College
