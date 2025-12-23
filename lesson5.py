#!/opt/anaconda3/bin/python
import bs4 as bs
import pickle
import requests


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
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)

    return tickers


save_sp500_tickers()

# https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
