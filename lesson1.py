import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
# import pandas_datareader.data as web
import yfinance as yf


style.use('ggplot')
start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

# df = web.DataReader('TSLA', 'yahoo', start, end)
df = yf.download('TSLA', start, end, True)
print(df.head())