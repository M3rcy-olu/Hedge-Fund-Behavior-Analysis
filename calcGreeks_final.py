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
#Calculating Options Greeks
def calc_greeks(call_option, experiation_date, type):
    expiration_date_num = ''
    for character in expiration_date: 
        if character != '-':
            expiration_date_num += character

    expiration_date_num = dt.strptime(expiration_date_num, '%Y%m%d').date()
    today = date.today()
    time = expiration_date_num - today
    time = time.days #this is the maturity time in days
    time = time/365 # this is the maturity time in terms of years

    risk_free_rate = 0.0525
    u_price =  stock_price[-1]
    strike_p = call_option[index_header_dict['strike']]
    vol = call_option[index_header_dict['impliedVolatility']]

    
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
stock_price = stock_price.iloc[:, 3].values.tolist()

#gets all the expirations dates for the ticker and puts it in a single coloumn data fram
expiration_dates = pd.DataFrame(ticker.options)
expiration_date = expiration_dates.loc[2][0]


#gets all call and put options for the selected expiration date
options_chain_calls = pd.DataFrame(ticker.option_chain(expiration_date).calls)
options_chain_puts = pd.DataFrame(ticker.option_chain(expiration_date).puts)
options_chain_calls.iloc[:, 1] = "N/A"
options_chain_puts.iloc[:, 1] = 'N/A'

#print(options_chain_calls)
df_header = options_chain_calls.columns.values.flatten()

#empty lists to contain calculated values of options greeks
deltas = []
gammas = []
vegas = []
rhos = []
thetas = []

#calculates greeks for all call options within the option chain of 1 expriation date
num_options = len(options_chain_calls)
counter = 0
while (counter < num_options):
    call_option = options_chain_calls.loc[counter].values.flatten().tolist()
    greeks_list = calc_greeks(call_option, expiration_date, type = 'c')
    deltas.append(greeks_list[0])
    gammas.append(greeks_list[1])
    vegas.append(greeks_list[2])
    rhos.append(greeks_list[3])
    thetas.append(greeks_list[4])
    counter+=1

greeks_table = pd.DataFrame({'Delta':deltas, 'Gamma':gammas, 'Vega':vegas, 'Rho': rhos, 'Theta': thetas})
final_table = pd.concat([options_chain_calls, greeks_table], axis=1)
final_table.to_excel('calls_output.xlsx', sheet_name= ticker_text + " " + expiration_date)


deltas = []
gammas = []
vegas = []
rhos = []
thetas = []

#calculates greeks for all put options and puts it in different xlsx sheet
num_options = len(options_chain_puts)
counter = 0
while (counter < num_options):
    put_option = options_chain_puts.loc[counter].values.flatten().tolist()
    greeks_list = calc_greeks(put_option, expiration_date, type = 'p')
    deltas.append(greeks_list[0])
    gammas.append(greeks_list[1])
    vegas.append(greeks_list[2])
    rhos.append(greeks_list[3])
    thetas.append(greeks_list[4])
    counter+=1

greeks_table = pd.DataFrame({'Delta':deltas, 'Gamma':gammas, 'Vega':vegas, 'Rho': rhos, 'Theta': thetas})
final_table = pd.concat([options_chain_puts, greeks_table], axis=1)
final_table.to_excel('puts_output.xlsx', sheet_name= ticker_text + " " + expiration_date)

print('done')












