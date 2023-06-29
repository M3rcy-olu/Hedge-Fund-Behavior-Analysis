import yfinance as yf
from openpyxl import load_workbook
import datetime as dt
from datetime import date

#Calculates return from 30 min before stock market closes to current close.
def get_sheetnames_xlsx(filepath): 
    wb = load_workbook(filepath, read_only=True, keep_links=False)
    return wb.sheetnames

sheet_name = get_sheetnames_xlsx('calls_output.xlsx')
sheet_name = sheet_name[0].split()

expiration_date = sheet_name[1]

ticker_text = sheet_name[0]
ticker = yf.Ticker(ticker_text)

stock_data = ticker.history()

stock_closes = stock_data.iloc[:, 3].values.tolist()
stock_opens = stock_data.iloc[:, 0].values.tolist()
prev_close_p = stock_closes[-2]
current_p = stock_closes[-1]
current_return =  (current_p - prev_close_p) / prev_close_p

