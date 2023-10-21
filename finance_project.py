# -*- coding: utf-8 -*-
"""Finance_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XJMeIIp4kPtS9WMU_OSO71OmAdhMMH_D
"""

!pip install pandas-datareader

# Commented out IPython magic to ensure Python compatibility.
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
# %matplotlib inline

"""# WE will get stock information of the following banks Bank of America,CitiGroup,Goldman Sachs,JPMorgan Chase, MorganStanley,Wells Fargo"""

data_BAC= pd.read_csv('/content/BAC.csv')
data_C= pd.read_csv('/content/C.csv')
data_GS= pd.read_csv('/content/GS.csv')
data_JPM= pd.read_csv('/content/JPM.csv')
data_MS= pd.read_csv('/content/MS.csv')
data_WFC= pd.read_csv('/content/WFC.csv')

data_BAC.head()

data_C.head()

tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

data_BAC.set_index('Date',inplace=True)
data_C.set_index('Date',inplace=True)
data_GS.set_index('Date',inplace=True)
data_JPM.set_index('Date',inplace=True)
data_MS.set_index('Date',inplace=True)
data_WFC.set_index('Date',inplace=True)

bank_stocks = pd.concat([data_BAC, data_C, data_GS, data_JPM, data_MS, data_WFC],axis=1,keys=tickers)

bank_stocks.head()

bank_stocks.columns.names = ['Bank Ticker','Stock Info']

bank_stocks.head()

"""#What is the max Close price for each bank's stock throughout the time period?"""

max_close_price= bank_stocks.xs('Close',level='Stock Info',axis=1).max()
max_close_price

"""#In pandas, the pct_change() function is used to calculate the percentage change between consecutive elements in a Series or DataFrame. So we will caculate the returns of the stocks using this function."""

returns= pd.DataFrame()

for tick in tickers:
  returns[tick+'Return']= bank_stocks[tick]['Close'].pct_change()
returns

returns=returns.iloc[1:]
returns

import seaborn as sns
sns.set_style("whitegrid")
sns.pairplot(returns)

# Worst single day returns in all banks
returns.idxmin()

#Best single day returns in all banks
returns.idxmin()

returns.std() # CReturns is more risky stock

sns.displot(returns['BACReturn'],bins=100,color='green')

sns.displot(returns['GSReturn'],color='red',bins=150)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()

"""# Line plots of closing price of each bank during the whole time period"""

bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot()

sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

close_corr = bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr()
# close_corr.iplot(kind='heatmap',colorscale='rdylbu')

"""# Rolling mean on 21 days, help to filter or smooth data by removing unwanted noise and variaions."""

plt.figure(figsize=(12,6))
data_BAC['Close'].rolling(window=21).mean().plot(label='21 Day Avg')
data_BAC['Close'].plot(label='BAC CLOSE')
plt.legend()

plt.figure(figsize=(12,6))
data_BAC['Close'].rolling(window=21).mean().plot(label='21 Day Rolling Avg of BAC')
data_C['Close'].rolling(window=21).mean().plot(label='21 Day Rolling Avg of C')
plt.legend()

"""# rolling standard deviation of 21 days of daily returns"""

plt.figure(figsize=(12,6))
data_BAC['Close'].rolling(window=21).std().plot(label='21 Day Avg of BAC')
data_C['Close'].rolling(window=21).std().plot(label='21 Day Avg of C')
plt.legend()

plt.figure(figsize=(12,6))
data_GS['Close'].rolling(window=21).mean().plot(label='21 Day Std of GS')
data_JPM['Close'].rolling(window=21).mean().plot(label='21 Day Std of JPM')
plt.legend()

"""# To find rolling correlation of two stocks

"""

plt.figure(figsize=(12,6))
bank_stocks['BAC']['Close'].rolling(window=21).corr(bank_stocks['C']['Close']).plot(label='Rolling_corr of BAC and C')
plt.legend()

rolling_corr= bank_stocks['BAC']['Close'].rolling(window=21).corr(bank_stocks['C']['Close'])
plt.hist(rolling_corr, bins=30)  # Adjust the number of bins as per your preference
plt.xlabel('Correlation')
plt.ylabel('Frequency')
plt.title('Histogram of 21-day Rolling Correlation')
plt.grid(True)
plt.show()

