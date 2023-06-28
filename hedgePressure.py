import pandas as pd
import yfinance as yf
from openpyxl import load_workbook

with open('calcGreeks_final.py') as f: 
    exec(f.read())

#Dictionary to easily access the columns/indecies for each component (ex: strike price)
header_dict = {
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
    'delta' : 14, 
    'gamma' : 15, 
    'vega' : 16, 
    'rho' : 17, 
    'theta' : 18

}

#Defines functions
def get_sheetnames_xlsx(filepath): 
    wb = load_workbook(filepath, read_only=True, keep_links=False)
    return wb.sheetnames

def calc_dol_gamma(option, option_type):
    gamma = option[header_dict['gamma']]
    open_interest = option[header_dict['openInterest']]
    if option_type == 'p': 
        dollar_gamma =  -1 * gamma * open_interest * 100 * underlying_p
    else: 
        dollar_gamma = gamma * open_interest * 100 * underlying_p
    return dollar_gamma

def calc_gamma_imb(ticker, call_dollar_gammas, put_dollar_gammas): 
    vol_history = ticker.history(period= '1mo')

    total_dol_vol = 0
    max_counter = len(vol_history)
    counter = 0 
    while (counter < max_counter): 
        vol_history[vol_history.columns[5]] = vol_history[vol_history.columns[5]].astype(int)
        vol = vol_history.iloc[counter, 5]
        vol_history[vol_history.columns[4]] = vol_history[vol_history.columns[4]].astype(int)
        price = vol_history.iloc[counter, 4]
        total_dol_vol += vol * price
        counter += 1

    avg_dol_vol = total_dol_vol / max_counter


    total_call_g = 0 
    total_put_g = 0

    for g in call_dollar_gammas:
        total_call_g += g

    for m in put_dollar_gammas: 
        total_put_g += m 

    gamma_imb = (total_call_g + total_put_g) * (underlying_p/100) * (1/avg_dol_vol)
    return gamma_imb

#Overall gathers data from excel sheets
#Initializes variables for stock name and experiation date. 
#Converts Excel to dataframe 
sheet_name = get_sheetnames_xlsx('calls_output.xlsx')
sheet_name = sheet_name[0].split()

expiration_date = sheet_name[1]

ticker_text = sheet_name[0]
ticker = yf.Ticker(ticker_text)

stock_price = ticker.history()
stock_price = stock_price.iloc[:, 3].values.tolist()
underlying_p = stock_price[-1]
call_chain = pd.read_excel('calls_output.xlsx')
call_chain = call_chain.drop(call_chain.columns[0], axis = 1)
put_chain = pd.read_excel('puts_output.xlsx')
put_chain = put_chain.drop(put_chain.columns[0], axis = 1)

call_dollar_gammas = []
put_dollar_gammas = []


#Execution function to calculate dollar gammas 
#Dollar gamma = gamma * open interest * 100 * latest underlying price --> for an option on the experiation date from the excel sheet for each strike price
num_options = len(call_chain)
counter = 0
while (counter < num_options):
    call_option = call_chain.loc[counter].values.flatten().tolist()
    call_dol_gamma = calc_dol_gamma(call_option, 'c')
    call_dollar_gammas.append(call_dol_gamma)
    counter += 1

num_options = len(put_chain)
counter = 0
while (counter < num_options):
    put_option = put_chain.loc[counter].values.flatten()
    put_dol_gamma = calc_dol_gamma(put_option, 'p')
    put_dollar_gammas.append(put_dol_gamma)
    counter+=1

gamma_imb = calc_gamma_imb(ticker, call_dollar_gammas, put_dollar_gammas)

print(expiration_date)
print(gamma_imb)



#Combines calculated dollar gammas with Dataframe of options data
call_dollar_gammas = pd.DataFrame({'Dollar Gamma': call_dollar_gammas})
call_chain = pd.concat([call_chain, call_dollar_gammas], axis=1)

put_dollar_gammas = pd.DataFrame({'Dollar Gamma': put_dollar_gammas})
put_chain = pd.concat([put_chain, put_dollar_gammas], axis=1)

call_chain.to_excel('calls_dol_gammas.xlsx', sheet_name= ticker_text + " " + expiration_date)
put_chain.to_excel('puts_dol_gammas.xlsx', sheet_name= ticker_text + " " + expiration_date)

