# from __future__ import (absolute_import, division, print_function,
#                         unicode_literals)

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.markers as mark
import tensorflow as tf
import sys
from sklearn.preprocessing import MinMaxScaler
import math
from pandas_datareader import data as web
import yfinance as yf
from datetime import datetime
from datetime import timezone
from time import time, sleep
import requests
import seaborn as sns

from tensorflow import keras
from keras import Sequential
# from tensorflow.keras.layers import Dense, LSTM
from keras_tuner import HyperModel
from keras_tuner.tuners import RandomSearch 
from keras_tuner.tuners import Hyperband 
from pylab import rcParams

import backtrader as bt
import argparse
import backtrader.feeds as btfeeds
import os.path

ticker = "NOW" # specific asset to fetch data for
granularity = "1d" # time interval for data collection

# number of days model is looking back
lookback = 60

# split training data into three distinct UTC time ranges to prevent data leakage
parameter_tuning_start = int(datetime(2012, 7, 20).replace(tzinfo=timezone.utc).timestamp())
parameter_tuning_end = int(datetime(2016, 12, 31).replace(tzinfo=timezone.utc).timestamp())

model_training_start = int(datetime(2017, 1,1).replace(tzinfo=timezone.utc).timestamp())
model_training_end = int(datetime(2020, 12, 31).replace(tzinfo=timezone.utc).timestamp())

backtest_start = int(datetime(2021, 1,1).replace(tzinfo=timezone.utc).timestamp())
backtest_end = int(datetime(2025, 1, 5).replace(tzinfo=timezone.utc).timestamp())

# find optimal slow and fast window periods
slow_start = 20
slow_end = 150
slow_step = 10

fast_start = 20
fast_end = 150
fast_step = 10

# api key
data = yf.download(
    ticker,
    start=parameter_tuning_start,
    end=parameter_tuning_end,
    interval=granularity,
    group_by="ticker"
)
data = pd.DataFrame(data)

'''
backtesting - using historical data to evaluate model performance
Backtrader offers way for traders to test algorithms with visualization, data feeds, etc
'''

backtrader_data = data.reset_index()
backtrader_data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

backtrader_data['openinterest'] = 0

plt.plot(backtrader_data['date'], backtrader_data['close'])
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Close Price Over Time')
plt.show()

'''
BASELINE PARAMETER PERFORMANCE
'''

res = []
# cerebro object orchestrates everything to run backtests - add strategies, act as brokers, analyze, etc.
cerebro = bt.Cerebro(stdstats = False, maxcpus = None)
cerebro.broker.setcash(250000)

data=bt.feeds.PandasData(dataname=backtrader_data, datetime='date')
cerebro.adddata(data)
# %%
