import yfinance as yf
import pandas as pd

def get_ticker_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start, end, actions=False, auto_adjust=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel('Ticker')
    df.columns.name = None

    return df