#yfinance data and dataframe managing
import requests
import yfinance as yf
import mibian as mibian
import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import date

#nasdaq webscrapping
from bs4 import BeautifulSoup
from selenium import webdriver
import time


stock_ticker = 'SPY'
ticker = yf.Ticker(stock_ticker)

#gets all the expirations dates for the ticker and puts it in a single coloumn data fram
expiration_dates = pd.DataFrame(ticker.options)
expiration_date = expiration_dates.loc[2][0]
print(expiration_dates)

#gets all call and put options for the selected expiration date
options_chain_calls = pd.DataFrame(ticker.option_chain(expiration_date).calls)
options_chain_puts = pd.DataFrame(ticker.option_chain(expiration_date).puts)
#print(options_chain_calls)

r = requests.get('https://www.nasdaq.com/market-activity/etf/spy/option-chain-greeks')
soup = BeautifulSoup(r, 'lxml')
print(r)