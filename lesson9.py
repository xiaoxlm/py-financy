#!/opt/anaconda3/bin/python
from re import A
import bs4 as bs
import pickle
import requests
import os
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import seaborn as sns


def process_data_for_labels(ticker: str) -> tuple[list[str], pd.DataFrame]:
    hm_days: int = 7  # 预测未来 7 天的价格变化
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)  # 读取所有股票的收盘价数据
    tickers = df.columns.values.tolist()  # 获取所有股票代码列表
    df.fillna(0, inplace=True)  # 将缺失值填充为 0

    # 为未来 1-7 天创建价格变化率列（标签）
    for i in range(1, hm_days + 1):
        # shift(1) = 昨天；shift(2) = 前天；shift(-1) = 明天；shift(-2) = 后天
        tomorrow_price = df[ticker].shift(-i)
        today_price = df[ticker]
        # 计算未来第 i 天相对于今天的价格变化率（百分比）；
        df['{}_{}d'.format(ticker, i)] = (tomorrow_price - today_price) / today_price

    df.fillna(0, inplace=True)

    return tickers, df


process_data_for_labels('XOM')
# 这个方法要做的事如下：
# 日期        今天价格  未来价格  计算公式              结果(XOM_1d)
# 2020-01-01  100      102      (102-100)/100      = 0.02  (涨2%)
# 2020-01-02  102      98       (98-102)/102       = -0.039 (跌3.9%)
# 2020-01-03  98       105      (105-98)/98        = 0.071 (涨7.1%)
# 2020-01-04  105      103      (103-105)/105      = -0.019 (跌1.9%)
# 2020-01-05  103      NaN      NaN                = NaN

def buy_sell_hold(*args, **kwargs):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if args[col] > requirement:
            return 1
        elif args[col] < -requirement:
            return -1
        else:
            return 0