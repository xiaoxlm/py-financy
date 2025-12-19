#!/opt/anaconda3/bin/python
import pandas as pd
import mplfinance as mpf

# 读取数据
df = pd.read_csv('tsla.csv', index_col=0, parse_dates=True)

# 重采样为10天的 OHLC 数据(10日k线图)
# mplfinance 需要标准的 OHLC 列名：Open, High, Low, Close, Volume
df_resampled = pd.DataFrame()
df_resampled['Open'] = df['Open'].resample('10D').first()   # 每10天的第一个开盘价
df_resampled['High'] = df['High'].resample('10D').max()     # 每10天的最高价
df_resampled['Low'] = df['Low'].resample('10D').min()       # 每10天的最低价
df_resampled['Close'] = df['Close'].resample('10D').last()  # 每10天的最后收盘价
df_resampled['Volume'] = df['Volume'].resample('10D').sum() # 每10天的成交量总和

# 删除空值
df_resampled.dropna(inplace=True)

print(df_resampled.head())

# 绘制蜡烛图（K线图）
# type='candle' 表示蜡烛图
# volume=True 表示显示成交量
# style='charles' 是一种配色方案，也可以用 'yahoo', 'nightclouds' 等
mpf.plot(df_resampled, 
         type='candle',           # 蜡烛图(绿涨红跌)
         volume=True,             # 显示成交量
         style='charles',         # 图表风格
         title='TSLA 10-Day OHLC',
         ylabel='Price ($)',
         ylabel_lower='Volume')