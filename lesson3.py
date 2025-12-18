import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style

style.use('ggplot')

df = pd.read_csv('tsla.csv', index_col=0, parse_dates=True)

df['100ma'] = df['Adj Close'].rolling(window=100,
                                      min_periods=0).mean()  # ma = moving average； 请计算过去100天的平均值，即百日均线(window=100)，但是！ 如果数据不够100个，哪怕只有1个数据（min_periods=0），也请尽量算出来
# df.dropna(inplace=True)
print(df.head())

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)  # ax2跟着 ax1联动(sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()
