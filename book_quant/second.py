#!/opt/anaconda3/bin/python

# 包含 最无脑的交易高抛低吸策略的回测方法、双移动平均策略、双移动平均策略的回测方法

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将父目录添加到 Python 路径中
from util.ticker import get_ticker_data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# start_data = '2020-01-01'
# end_data = '2020-03-21'

# ticker_num = '601318.ss'

# df_data = get_ticker_data(ticker_num, start_data, end_data)

# df_data.to_csv("601318.ss.csv")
# print(df_data.head())

# 最无脑的交易高抛低吸策略的回测方法
def backtest_strategy_simplest(df_data: pd.DataFrame):
    df_data_signal = pd.DataFrame(index=df_data.index)  # 只保留数据中的日期
    # df_data_signal['price'] = df_data['Adj Close']
    df_data_signal['price'] = df_data['Close']
    df_data_signal['diff'] = df_data_signal['price'].diff()

    df_data_signal = df_data_signal.fillna(0.0)  # 第一行会出现空值，用0.0来补填

    df_data_signal['signal'] = np.where(df_data_signal['diff'] >= 0, 0, 1)  # 股价下跌标记为1
    # oder(下单)
    df_data_signal['order'] = df_data_signal['signal'].diff() * 100  # 根据交易信号的变化进行下单。100为A股的一手

    # 回测
    initial_cash = 20000.00  # 初始资金

    # cumsum()函数用于逐步累加前面的数值，返回一个按行累加的序列。例如[1,2,3].cumsum()结果为[1,3,6]。
    df_data_signal['virtual_cash'] = initial_cash - (
                df_data_signal['order'].diff() * df_data_signal['price']).cumsum()  # 买完股票后，剩余资金(净值)

    df_data_signal['stock'] = df_data_signal['order'] * df_data_signal[
        'price']  # 持仓股数的市值(卖出就相当于是负值，这个值会加在 virtual_cash 中)

    df_data_signal['total'] = df_data_signal['stock'] + df_data_signal['virtual_cash']  # 总资产 = 股票市值 + 剩余资金

    print(df_data_signal.head())

    plt.figure(figsize=(10, 6))
    plt.plot(df_data_signal['total'], label='total assets')  # 总资产
    plt.plot(df_data_signal['order'].cumsum() * df_data_signal['price'], '--', label='stock value')
    plt.grid()
    plt.legend(loc='center right')
    plt.show()


# 画10日平均线
def draw_avg_value_10(df_data: pd.DataFrame):
    period: int = 10  # 10日均线
    avg_10: list[float] = []  # 存储每10天价格
    avg_value: list[float] = []  # 存储每10天价格的平均值

    for price in df_data['Close']:
        avg_10.append(price)
        if len(avg_10) > period:
            # del avg_10[0]
            avg_10.pop(0)

        avg_value.append(np.mean(avg_10))  # 将10天数据的均值传入列表中

    df_data = df_data.assign(avg_10=pd.Series(avg_value, index=df_data.index))

    plt.figure(figsize=(10, 6))
    plt.plot(df_data['Close'], lw=2, c='k', label='Close')
    plt.plot(df_data['avg_10'], '--', lw=2, label='avg_10')
    plt.legend(loc='center right')  # 添加图注和网格
    plt.grid()
    plt.show()


# 双移动平均策略
def strategy_double_avg_value_5_10(df_data: pd.DataFrame, draw: bool = False) -> pd.DataFrame:
    strategy: pd.DataFrame = pd.DataFrame(index=df_data.index)
    strategy['signal'] = 0
    strategy['avg_5'] = df_data['Close'].rolling(window=5).mean()
    strategy['avg_10'] = df_data['Close'].rolling(window=10).mean()
    strategy['signal'] = np.where(strategy['avg_5'] > strategy['avg_10'], 1, 0)
    strategy['order'] = strategy['signal'].diff()
    
    if draw:
        plt.figure(figsize=(10, 5))
        plt.plot(df_data['Close'], lw=2, c='k', label='price')
        plt.plot(strategy['avg_5'], ls='--', label='avg_5')
        plt.plot(strategy['avg_10'], ls='-.', label='avg_10')

        plt.scatter(strategy.loc[strategy.order == 1].index,
                    df_data['Close'].loc[strategy.order == 1],
                    c='r',
                    marker='^',
                    s=80,
                    label='buy')
        plt.scatter(strategy.loc[strategy.order == -1].index,
                    df_data['Close'].loc[strategy.order == -1],
                    c='g',
                    marker='v',
                    s=80,
                    label='sell')

        plt.legend(loc='center right')
        plt.grid()
        plt.show()

    return strategy

def backtest_strategy_double_avg_value_5_10(df_data: pd.DataFrame, strategy: pd.DataFrame):
    initial_cash: float = 20000.00
    positions: pd.DataFrame = pd.DataFrame(index=strategy.index).fillna(0.0)
    positions['stock'] = strategy['signal'] * 100

    portfolio: pd.DataFrame = pd.DataFrame(index=strategy.index).fillna(0.0)
    portfolio['stock value'] = positions.multiply(df_data['Close'], axis=0)

    order = positions.diff()

    portfolio['cash'] = initial_cash - (order.multiply(df_data['Close'], axis=0)).cumsum()
    portfolio['total'] = portfolio['stock value'] + portfolio['cash']

    print(portfolio.tail(10))

    plt.figure(figsize=(10, 5))
    plt.plot(portfolio['total'], lw=2, label='total assets')
    plt.plot(portfolio['stock value'], lw=2, ls='--', label='stock value')
    plt.legend(loc='center right')
    plt.grid()
    plt.show()

df_data = pd.read_csv('601318.ss.csv', index_col=0, parse_dates=True)
strategy = strategy_double_avg_value_5_10(df_data)
backtest_strategy_double_avg_value_5_10(df_data, strategy)
