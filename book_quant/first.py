import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 将父目录添加到 Python 路径中
from util.ticker import get_ticker_data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# print(web.__version__)

# start_data = '2020-01-01'
# end_data = '2020-03-18'

# ticker_num = '601318.ss'

# df_data = get_ticker_data(ticker_num, start_data, end_data)

# df_data.to_csv("601318.ss.csv")
df_data = pd.read_csv('601318.ss.csv', index_col=0, parse_dates=True)

df_data['diff'] = df_data['Close'].diff()

df_data['Signal'] = np.where(df_data['diff'] > 0, 1, 0)

# print(df_data.head())
plt.figure(figsize=(10, 5))# 设置画布尺寸 10 * 5

df_data['Close'].plot(linewidth=2, color='k', grid=True) # 使用折线图绘制出每天的收盘价
# 如果当天股价上涨，标出卖出信号，用倒三角表示
plt.scatter(
    df_data['Close'].loc[df_data['Signal'] == 1].index,
    df_data['Close'].loc[df_data['Signal'] == 1],
    marker='v',              # 用倒三角表示卖出信号
    s=80,                    # s=80 表示散点（marker）的面积大小为80，这会影响三角形的视觉尺寸
    c='g',                   # 绿色，卖出信号
    label='Sell'
)

# 如果当天股价下跌给出买入信号，用正三角表示
plt.scatter(
    df_data['Close'].loc[df_data['Signal'] == 0].index,
    df_data['Close'].loc[df_data['Signal'] == 0],
    marker='^',              # 用正三角表示买入信号
    s=80,                    # s=80 表示散点（marker）的面积大小为80，这会影响三角形的视觉尺寸
    c='r',                   # 红色，买入信号
    label='Buy'
)

plt.show()
