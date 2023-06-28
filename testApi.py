#This program is to test getting stock options data from polygon as yfinance is not alway consistent
# Imports
from polygon import RESTClient
import datetime

#Initiate Client
client = RESTClient(api_key="3d1jrVRqJl_BsnlUtbWPka_9Ve3QMISB")

#Functions
#Spaces an option tiker symbol: Remember a ticker symbol containes the underlying stock price, the experiation date, strike price and etc. data
def spaceTicker(ticker):
    old_ticker = ticker
    ticker_length = len(ticker)
    strike_space = ticker_length - 8
    order_type_space = strike_space - 1 
    experiation_space = order_type_space - 6
    new_ticker = old_ticker[:experiation_space] + ',' + old_ticker[experiation_space:order_type_space] + ',' + old_ticker[order_type_space:strike_space] + ',' + old_ticker[strike_space:]
    return new_ticker

#converts information in a ticker price into a dictionary
def convertTicker(spaced_ticker):
    ticker_dict = {
        'root_symbol' : '',
        'experiation_date' : '', 
        'order_type' : '', 
        'strike_price' : '', 
    }

    sliced_ticker = spaced_ticker.split(',')
    comp_counter = 0
    for key in ticker_dict:
        ticker_dict[key] = sliced_ticker[comp_counter]
        comp_counter += 1

    ticker_dict['root_symbol'] = ticker_dict['root_symbol'].removeprefix('O:')
    temp_exp_date = '20' + ticker_dict['experiation_date'][:2] + '/' + ticker_dict['experiation_date'][2:4] + '/' + ticker_dict['experiation_date'][4:]
    format = '%Y/%m/%d'
    return ticker_dict


#Program/Testing



