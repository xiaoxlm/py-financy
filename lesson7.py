#!/opt/anaconda3/bin/python
from re import A
import bs4 as bs
import pickle
import requests
import os
import pandas as pd
import datetime as dt
import yfinance as yf


def save_ticker_data_to_csv(ticker: str, start: dt.datetime, end: dt.datetime) -> str:
    csv_file_path = 'stock_dfs/{}.csv'.format(ticker)
    if not os.path.exists(csv_file_path):
        df = yf.download(ticker, start, end, actions=False, auto_adjust=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel('Ticker')
            df.columns.name = None
            df.to_csv(csv_file_path)
            print('Saved {} successfully'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

    return csv_file_path


# S&P500 into one DataFrame
def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    main_df = pd.DataFrame()
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2016, 12, 31)

    for count, ticker in enumerate(tickers):
        csv_file_path = save_ticker_data_to_csv(ticker, start, end)

        # get ticker's data
        df = pd.read_csv(csv_file_path)
        df.set_index("Date",
                     inplace=True)  # 设置 Date为数据索引。 inplace=True = "直接在原变量上修改，不创建新变量"。现代 Python 社区更推荐不使用 inplace，因为更符合函数式编程的理念
        df.rename(columns={"Adj Close": ticker}, inplace=True)
        df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how="outer")  # 类似与 sql 的外连接(outer)。如果左表有，右表没有，则右表的值为 NaN。如果右表有，左表没有，则左表的值为 NaN。

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv("sp500_joined_closes.csv")


compile_data()
