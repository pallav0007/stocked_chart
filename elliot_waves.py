import numpy as np
from scipy.signal import argrelextrema
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from nsepy import get_history
import datetime
from collections import defaultdict
dt=datetime.date.today()
pd.options.display.max_columns=None
# def get_max_min(prices, smoothing, window_range):
#     smooth_prices = prices['Close'].rolling(window=smoothing).mean().dropna()
#     local_max = argrelextrema(smooth_prices.values, np.greater)[0]
#     local_min = argrelextrema(smooth_prices.values, np.less)[0]
#     price_local_max_dt = []
#     for i in local_max:
#         if (i>window_range) and (i<len(prices)-window_range):
#             price_local_max_dt.append(prices.iloc[i-window_range:i+window_range]['Close'].idxmax())
#     price_local_min_dt = []
#     for i in local_min:
#         if (i>window_range) and (i<len(prices)-window_range):
#             price_local_min_dt.append(prices.iloc[i-window_range:i+window_range]['Close'].idxmin())
#     maxima = pd.DataFrame(prices.loc[price_local_max_dt])
#     minima = pd.DataFrame(prices.loc[price_local_min_dt])
#     # max_min = pd.concat([maxima, minima]).sort_index()
#     # max_min.index.name = 'date'
#     # max_min = max_min.reset_index()
#     # max_min = max_min[~max_min.date.duplicated()]
#     # p = prices.reset_index()
#     # max_min['day_num'] = p[p.index.isin(max_min.date)].index.values
#     # max_min = max_min.set_index('day_num')['Close']
#
#     return maxima,minima
def plot_elliot(df):
    dat,dat2=get_max_min(df,3,10)
    fig6 = px.line(df, x=df.index, y="Close", hover_data=["Close", "Volume", "Low", "High"], title="ADX trend")
    fig6.add_scatter(name="+ dmi", x=dat.index, y=dat)
    fig6.add_scatter(name="- dmi", x=dat2.index, y=dat2)
    fig6.show()
dat=get_history(symbol="ADANIPORTS",
                           start=dt - datetime.timedelta(300),
                           end=dt)


def get_max_min(prices, smoothing, window_range):
    smooth_prices = prices['Close'].rolling(window=smoothing).mean().dropna()
    local_max = argrelextrema(smooth_prices.values, np.greater)[0]
    local_min = argrelextrema(smooth_prices.values, np.less)[0]
    price_local_max_dt = []
    for i in local_max:
        if (i > window_range) and (i < len(prices) - window_range):
            price_local_max_dt.append(prices.iloc[i - window_range:i + window_range]['Close'].idxmax())
    price_local_min_dt = []
    for i in local_min:
        if (i > window_range) and (i < len(prices) - window_range):
            price_local_min_dt.append(prices.iloc[i - window_range:i + window_range]['Close'].idxmin())
    maxima = pd.DataFrame(prices.loc[price_local_max_dt])
    minima = pd.DataFrame(prices.loc[price_local_min_dt])

    max_min = pd.concat([maxima, minima]).sort_index()
    max_min = max_min[~max_min.index.duplicated()]

    px.scatter(max_min,x=max_min.index,y=max_min["Close"])
    return max_min


def find_patterns(max_min):
    patterns = defaultdict(list)

    for i in range(5, len(max_min)):
        window = max_min.iloc[i - 5:i]
        # Pattern must play out in less than n units
        if (window.index[-1] - window.index[0]).days > 100:
            continue

        # a, b, c, d, e = window.iloc[0],window.iloc[1],window.iloc[2],window.iloc[3],window.iloc[4]

        # IHS
        a, b, c, d, e = window.iloc[0:5]["Close"]

        # IHS
        if a < b and c < a and c < e and c < d and e < d and abs(b - d) <= np.mean([b, d]) * 0.02:
            patterns['IHS'].append((window.index[0], window.index[-1]))
        # if window[(a < b) & (c < a) & (c < e) & (c < d) & (e < d) & (abs(b - d) <= np.mean([b, d]) * 0.02]):
        #     patterns['IHS'].append((window.index[0], window.index[-1]))

    return patterns


def plotit(patterns,max_min):
    fig = go.Scatter(x=max_min.index,y=max_min["Close"],line={'color': 'yellow'})
    data=[]
    for name, end_day_nums in patterns.items():
        for i, tup in enumerate(end_day_nums):
            sd = tup[0]
            ed = tup[1]

            # fig.line(x=max_min.loc[sd:ed].index,y=max_min.loc[sd:ed]["Close"])
    return fig

g=get_max_min(dat,3,10)
p=find_patterns(g)
plotit(p,g)