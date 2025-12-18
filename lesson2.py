import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style

style.use('ggplot')
# start = dt.datetime(2000, 1, 1)
# end = dt.datetime(2016, 12, 31)
#
# df = yf.download('TSLA', start, end, actions=False, auto_adjust=False)
# if isinstance(df.columns, pd.MultiIndex):
#     df.columns = df.columns.droplevel('Ticker')
# df.columns.name = None
#
# df.to_csv("tsla.csv")# 将数据转换成 csv 文件

df = pd.read_csv('tsla.csv', index_col=0, parse_dates=True)
# print(df.head())

# df.plot() # 全列数据展示
df['Adj Close'].plot()  # 一列
df[['High', 'Open']].plot()  # 只展示某些 列
plt.show()

# print(df['Adj Close']) #打印某一列
