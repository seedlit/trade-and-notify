
"""
Author: Naman Jain
        naman.jain@btech2015.iitgn.ac.in
        www.namanji.wixisite.com/naman/

This script plots candlesticks of the input stock symbols list and 
sends message and email notification if certain price threshold is breached.
One needs to have finnhub api token (freely available) to get plots
and twilio account (in order to send message notifications)
Before starting, it is recommended to go through finnhub api documentation
https://finnhub.io/docs/api
"""
#-----------------------------------------------------------------------------------------
# TODO: Add functions for identifying technical patterns.
#       Add voume monitoring, technical indicators functionality
#       Add futures and options functionality
#       Add % change in price
#       Set alerts for anything anomal (abnormal) for all stocks; ref: cox and kings 10paise fall
#       Calculate beta; refer chaper 11, module 4 of Zerodha varsity
#       Calculate volatility; refer chaper 16, module 5 of zerodha varsity
#       Implement Black and Scholes option pricing model


# Necessary imports
import time
import requests
import json
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Defining functions
def get_quote(url, stock_symbol):
    try:
      temp = requests.get(url)
      quote = json.loads(temp.content)    
      print('stock: {}; current price = {}; open = {}; high = {}; low = {}; previous close = {}'.format(stock_symbol, quote['c'], quote['o'], quote['h'], quote['l'], quote['pc']))
      return quote['c']
    except Exception as e:
      print('some issue in {}: {}'.format(stock_symbol, e))


def plot_candles(url, count, stock_symbol):
    try:
      df = pd.read_csv(url)
      fig = go.Figure(data=[go.Candlestick(x=df['t'], open=df['o'], high=df['h'], low=df['l'], close=df['c'])]) # c is current price
      fig.update_layout(title='Last {} candle sticks of {}'.format(count, stock_symbol), xaxis_title='time', yaxis_title='price', 
                        font=dict(family="Courier New, monospace",size=18, color="#7f7f7f"))    
      fig.show() 
    except Exception as e:
      print('some issue in {}: {}'.format(stock_symbol, e))


def plot_moving_avg(url):
    df = pd.read_csv(url)
    mavg = df['c'].ewm(span=26).mean()
    mavg1 = df['c'].ewm(span=12).mean()
    mavg.plot(ax=ax1,label='50_ema')
    mavg1.plot(color='k',ax=ax1, label='13_ema')


def get_support_resistance(url, stock_symbol): # weight=5
    try:
      temp = requests.get(url)
      support_resistance = json.loads(temp.content)
      print('support and resistance of {} = {}'.format(stock_symbol, support_resistance['levels']))
    except Exception as e:
      print('some issue in {}: {}'.format(stock_symbol, e))


def send_message(to_num, from_num, message, twilio_account_sid, twilio_auth_token):
    try:
      import twilio
      from twilio.rest import Client
      client = Client(twilio_account_sid, twilio_auth_token)
      client.messages.create(to= to_num, from_=from_num, body = message)
    except Exception as e:
      print('Some problem occured in sending message: {}'.format(e))


def send_email(gmail_id, gmail_pass, message, to_email_id):    
    try:
      import smtplib
      s = smtplib.SMTP('smtp.gmail.com', 587)   # creates SMTP session   
      s.starttls()   # start TLS for security   
      s.login(gmail_id, gmail_pass)   # Authentication      
      s.sendmail(gmail_id, to_email_id, message)   # sending the mail   
      s.quit()# terminating the session   
    except Exception as e:
      print('Some error occured in sending email: {}'.format(e))


def get_date_from_unix(unix_time_stamp):    
    ist_time_stamp = unix_time_stamp + (5.5 * 3600)
    date_and_time = datetime.utcfromtimestamp(ist_time_stamp).strftime('%d-%m-%Y %H:%M:%S')
    print(date_and_time)

#-------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # API related details
    # Upto 60 requests/minute for free account (with upper cap on 30 requests/sec)
    token = ''                 # finnhub api token
    stock_list = ['NIFTY', 'BANKNIFTY', 'AJANTPHARM','HEROMOTOCO','INDUSINDBK','LT','MARUTI','OIL','ONGC','SBICARD','SBIN','TCS','YESBANK', 'IRCTC', 'AARTIIND']
    resolution = 'D'           # supported resolution values: 1, 5, 15, 30, 60, D, W, M
    num_candles = 45           # number of candles to retreive with the latest one being the last one
    twilio_account_sid = ''
    twilio_auth_token = ''
    send_message_to = ''       # Mobile number (with country code) on which the notification will be received
    send_message_from = ''     # Mobile number (with country code) with which the notification will be received. Given by twilio
    gmail_id = ''              # gmail id from which email will be sent
    gmail_pass = ''            # gmail id password
    send_email_to = ''         # email address to which the notification will be received

    # Updating stock symbols for NSE (National Stock Exchange)
    for i in range(len(stock_list)):
      stock_list[i] += '.NS'

    # plotting candles   
    for stock_symbol in stock_list:
      quote_url = 'https://finnhub.io/api/v1/quote?symbol={}&token={}'.format(stock_symbol, token)  # returns c (current), h, l, o, pc (previous close), t
      candle_url = 'https://finnhub.io/api/v1/stock/candle?symbol={}&token={}&resolution={}&count={}&format=csv&adjusted=true'.format(stock_symbol, token, resolution, num_candles)
      support_resistance_url = 'https://finnhub.io/api/v1/scan/support-resistance?symbol={}&token={}&resolution={}'.format(stock_symbol, token, resolution)
      get_quote(quote_url, stock_symbol)
      get_support_resistance(support_resistance_url, stock_symbol)
      plot_candles(candle_url, num_candles, stock_symbol)
      time.sleep(5)  # time delay to avoid exhausting free api quota    

    # # setting price alert for Maruti
    # count = 0
    # while True:
    #   maruti_alert_quote_url = 'https://finnhub.io/api/v1/quote?symbol={}&token={}'.format('MARUTI.NS', token)
    #   maruti_current_price = get_quote(maruti_alert_quote_url, 'MARUTI.NS')
    #   hero_alert_quote_url = 'https://finnhub.io/api/v1/quote?symbol={}&token={}'.format('HEROMOTOCO.NS', token)    
    #   if count <= 5:
    #     if maruti_current_price <= 5360 or maruti_current_price >= 5400:
    #       message = 'Maruti price threshold breached!'
    #       send_message(send_message_to, send_message_from, message, twilio_account_sid, twilio_auth_token)
    #       count += 1      
    #   time.sleep(10)

    # # Defining various URLs
    # price_target = 'https://finnhub.io/api/v1/stock/price-target?symbol={}&token={}'.format(stock_symbol, token)
    # pattern_recognition = 'https://finnhub.io/api/v1/scan/pattern?symbol={}&resolution=D&token={}'.format(stock_symbol, token) # weight = 5
    # #  pattern recogition may return more than one patterns in form of separate dicts in points. 
    # quote = 'https://finnhub.io/api/v1/quote?symbol={}&token={}'.format(stock_symbol, token) 
    # candle = 'https://finnhub.io/api/v1/stock/candle?symbol={}&resolution=D&from=1575803199&to=1586804199&format=csv&token={}'.format(stock_symbol, token) 
    # divident = 'https://finnhub.io/api/v1/stock/dividend?symbol={}&from=2019-02-01&to=2020-02-01&token={}'.format(stock_symbol, token)
    # split = 'https://finnhub.io/api/v1/stock/split?symbol={}&from=2010-02-01&to=2020-02-01&token={}'.format(stock_symbol, token)
    # support_and_resistance = 'https://finnhub.io/api/v1/scan/support-resistance?symbol={}&resolution=D&token={}'.format(stock_symbol, token)
    # aggregate_indicators = 'https://finnhub.io/api/v1/scan/technical-indicator?symbol={}&resolution=D&token={}'.format(stock_symbol, token)
    # # technicalAnalysis: Number of indicator signals strong buy, buy, neutral, sell, strong sell signals.
    # # trend: Whether the market is trending.
    # technical_indicators = 'https://finnhub.io/api/v1/indicator?symbol={}&resolution=D&from=1583098857&to=1584308457&indicator=sma&timeperiod=3&token={}'.format(stock_symbol, token)    # like sma (simple moving average), etc.
    # # full list of indicators can be found here = https://docs.google.com/spreadsheets/d/1ylUvKHVYN2E87WdwIza8ROaCpd48ggEl1k5i5SgA29k/edit#gid=0    
    # crypto_candle = 'https://finnhub.io/api/v1/crypto/candle?symbol={}&resolution=D&from=1572651390&to=1575243390&format=csv&token={}'.format(crypto_symbol, token)
    # # info about company executives
    # company_executives = 'https://finnhub.io/api/v1/stock/executive?symbol={}&token={}'.format(stock_symbol, token)
    # # news about major developments
    # major_news = 'https://finnhub.io/api/v1/major-development?symbol={}&token={}'.format(stock_symbol, token) # weight = 10
    # major_news = 'https://finnhub.io/api/v1/major-development?symbol={}&from=2019-11-01&to=2020-02-15&token={}'.format(stock_symbol, token)  # weight = 10
    # # get company peers in same country
    # company_peers = 'https://finnhub.io/api/v1/stock/peers?symbol={}&token={}'.format(stock_symbol, token)
    # #  Get company key metrics such as growth, price, valuation.
    # # Full list of supported fields: https://static.finnhub.io/csv/metrics.csv
    # #  Metric type. Can be one of the following values price, valuation, growth, margin, management, financialStrength, perShare
    # company_metrics = 'https://finnhub.io/api/v1/stock/metric?symbol={}&metric=margin&token={}'.format(stock_symbol, token)   # weight = 5
    # # Investors Ownership: Get a full list of shareholders/investors of a company in descending order of the number of shares held.
    # # Weight: 20
    # investors_ownership = 'https://finnhub.io/api/v1/stock/investor-ownership?symbol={}&token={}&limit=20'.format(stock_symbol, token)
    # investors_ownership = 'https://finnhub.io/api/v1/stock/investor-ownership?symbol={}&token={}'.format(stock_symbol, token)
    # # Fund Ownership: Get a full list fund and institutional investors of a company in descending order of the number of shares held.
    # # Weight: 20
    # fund_ownership = 'https://finnhub.io/api/v1/stock/fund-ownership?symbol={}&token={}'.format(stock_symbol, token)