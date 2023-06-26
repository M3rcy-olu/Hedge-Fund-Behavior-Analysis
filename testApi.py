#Imports
from polygon import RESTClient
import datetime

#Initiate Client
client = RESTClient(api_key="3d1jrVRqJl_BsnlUtbWPka_9Ve3QMISB")

#Functions
def spaceTicker(ticker):
    old_ticker = ticker
    ticker_length = len(ticker)
    strike_space = ticker_length - 8
    order_type_space = strike_space - 1 
    experiation_space = order_type_space - 6
    new_ticker = old_ticker[:experiation_space] + ',' + old_ticker[experiation_space:order_type_space] + ',' + old_ticker[order_type_space:strike_space] + ',' + old_ticker[strike_space:]
    return new_ticker

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
ticker = "O:SPY251219C00650000"
spaced_ticker = spaceTicker(ticker)
ticker_dict = convertTicker(spaced_ticker)
print(ticker_dict)

'''ticker_info = {
    'under_stock' : ticker
}
bars = client.get_aggs(ticker=ticker, multiplier=1, timespan="day", from_="2023-01-09", to="2023-01-10")
for bar in bars:
    print(bar)'''


