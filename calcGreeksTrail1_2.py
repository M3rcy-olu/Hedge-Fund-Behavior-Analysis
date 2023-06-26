import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.implied_volatility import  implied_volatility as iv
from py_vollib.black_scholes.greeks.analytical import delta, gamma, vega, theta, rho
from datetime import datetime as dt
from datetime import date

index_header_dict = {
    'contractSymbol': 0,
    'lastTradeDate' : 1,
    'strike': 2,
    'lastPrice': 3,
    'bid' : 4,
    'ask' : 5,
    'change' : 6,
    'percentChange' : 7,
    'volume' : 8,
    'openInterest' : 9, 
    'impliedVolatility' : 10,
    'inTheMoney' : 11, 
    'contractSize' : 12,
    'currency' : 13,
}
#functions
def calc_iVol(call_option, experiation_date):
    expiration_date_num = ''
    for character in expiration_date: 
        if character != '-':
            expiration_date_num += character

    expiration_date_num = dt.strptime(expiration_date_num, '%Y%m%d').date()
    today = date.today()
    time = str(expiration_date_num - today)

    risk_free_rate = 0.0114
    u_price =  stock_price[-1]
    option_price = call_option[index_header_dict['lastPrice']]
    strike_p = call_option[index_header_dict['strike']]
    time = int(time[0])
    type = 'c'
    tol = 0.0001
    
    max_iter = 200
    vol_old = 0.3
    for k in range(max_iter): 
        bs_price = bs (type, u_price, strike_p, time, risk_free_rate, vol_old)
        Cprime = vega(type, u_price, strike_p, time, risk_free_rate, vol_old) * 100
        c = bs_price - option_price

        vol_new = vol_old - c/Cprime
        new_bs_price = bs (type, u_price, strike_p, time, risk_free_rate, vol_new)
        if (abs(vol_old - vol_new) < tol or abs(vol_old - option_price) < tol): 
            break
        vol_old = vol_new

    imp_v = vol_new
    return imp_v

#Calculating Options Greeks
def calc_greeks(call_option, experiation_date):
    expiration_date_num = ''
    for character in expiration_date: 
        if character != '-':
            expiration_date_num += character

    expiration_date_num = dt.strptime(expiration_date_num, '%Y%m%d').date()
    today = date.today()
    time = str(expiration_date_num - today)

    risk_free_rate = 0.0114
    u_price =  stock_price[-1]
    strike_p = call_option[index_header_dict['strike']]
    time = int(time[0])
    vol = call_option[index_header_dict['impliedVolatility']]

    type = 'c'
    
    #calculating Greeks
    delta_option = delta(type, u_price, strike_p, time, risk_free_rate, vol)
    gamma_option = gamma(type, u_price, strike_p, time, risk_free_rate, vol)
    vega_option = vega(type, u_price, strike_p, time, risk_free_rate, vol)
    rho_option = rho(type, u_price, strike_p, time, risk_free_rate, vol)
    theta_option = theta(type, u_price, strike_p, time, risk_free_rate, vol)

    delta_option = round(delta_option, 3)
    gamma_option = round(gamma_option, 3)
    vega_option = round(vega_option, 3)
    rho_option = round(rho_option, 3)
    theta_option = round(theta_option, 3)

    ''' print('Option Greeks:')
    print('delta: ', round(delta_option, 3))
    print('gamma: ', round(gamma_option, 3))
    print('vega: ', round(vega_option, 3))
    print('rho: ', round(rho_option, 3))
    print('theta: ', round(theta_option, 3))'''

    return delta_option, gamma_option, vega_option, rho_option, theta_option
   

#execution
ticker_text = 'SPY'
ticker = yf.Ticker(ticker_text)

stock_price = ticker.history()
stock_price = stock_price.iloc[:, 1].values.tolist()

#gets all the expirations dates for the ticker and puts it in a single coloumn data fram
expiration_dates = pd.DataFrame(ticker.options)
expiration_date = expiration_dates.loc[6][0]


#gets all call and put options for the selected expiration date
options_chain_calls = pd.DataFrame(ticker.option_chain(expiration_date).calls)
options_chain_puts = pd.DataFrame(ticker.option_chain(expiration_date).puts)
options_chain_calls.iloc[:, 1] = "N/A"
strikes = options_chain_calls.iloc[:, 2]
volatility = options_chain_calls.iloc[:, 10] 

#print(options_chain_calls)
df_header = options_chain_calls.columns.values.flatten()
#empty list to contain calculated implied volatility
i_vol = []

#empty lists to contain calculated values of options greeks
deltas = []
gammas = []
vegas = []
rhos = []
thetas = []

#calculates greeks for all options within the option chain of 1 expriation date
num_options = len(options_chain_calls)
counter = 0
while (counter < num_options):
    call_option = options_chain_calls.loc[counter].values.flatten().tolist()
    i_vol.append(calc_iVol(call_option, expiration_date))
    counter +=1

options_chain_calls.iloc[:,10] = i_vol

'''counter = 0
while (counter < num_options):
    call_option = options_chain_calls.loc[counter].values.flatten().tolist()
    greeks_list = calc_greeks(call_option, expiration_date)
    deltas.append(greeks_list[0])
    gammas.append(greeks_list[1])
    vegas.append(greeks_list[2])
    rhos.append(greeks_list[3])
    thetas.append(greeks_list[4])
    counter+=1

greeks_table = pd.DataFrame({'Delta':deltas, 'Gamma':gammas, 'Vega':vegas, 'Rho': rhos, 'Theta': thetas})
final_table = pd.concat([options_chain_calls, greeks_table], axis=1)

print(final_table)
final_table.to_excel('output.xlsx', sheet_name= ticker_text + " " + expiration_date)
print('done')
'''











