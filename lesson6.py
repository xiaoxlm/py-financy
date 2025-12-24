#!/opt/anaconda3/bin/python
import bs4 as bs
import pickle
import requests
import os
import pandas as pd
import datetime as dt
import yfinance as yf


def save_sp500_tickers() -> list[str]:
    # 添加 User-Agent 头部，避免被维基百科的反爬虫机制拦截（返回403）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', headers=headers)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'id': 'constituents'})
    tickers: list[str] = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.strip()  # 去除 ticker 末尾的换行符和多余空白
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers

# get all company pricing data in the S&P 500
def get_data_from_yahoo(reload_sp500=False):
    # get tickers
    tickers: list[str] = []
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2016, 12, 31)

    # get ticker's data
    for ticker in tickers:
        csv_file_path = "stock_dfs/{}.csv".format(ticker)
        if not os.path.exists(csv_file_path):
            df = yf.download(ticker, start, end, actions=False, auto_adjust=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel('Ticker')
            df.columns.name = None

            df.to_csv(csv_file_path)  # 将数据转换成 csv 文件
            print('Saved {} successfully'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


get_data_from_yahoo()
