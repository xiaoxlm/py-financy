import datetime as dt

import pandas as pd
import yfinance as yf
from matplotlib import style

style.use('ggplot')
start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

df = yf.download('ADBE', start, end, actions=False, auto_adjust=False)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel('Ticker')
df.columns.name = None
print(df.tail())
