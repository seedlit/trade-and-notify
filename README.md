# trade-and-notify
This repo monitors and plots Candlestick charts for stocks. Besides, it can also send notifications (message and email). I will update it to execute trading transactions as well.

## About
There are two scripts.
##### monitor_stocks_and_alert.py: 
This script plots candlesticks of the input stock symbols list and 
sends message and email notifications if certain price threshold is breached.
One needs to have finnhub api token (freely available) to get plots
and twilio account (in order to send message notifications). It supports all the stocks and exchanges available on finnhub.
Before starting, it is recommended to go through finnhub api documentation
https://finnhub.io/docs/api
##### stock_candlestick_patterns.py:
The aim of writing this script is to minimize my need to look at stock prices multiple times a day.
Rather these functions should be able to montior the stock prices and notify me if I should make a trading decision.
The patterns defined in this script are inspired from Zerodha's Varstity Module 2, 'Technical Analysis'.
Here is the link to the module - https://zerodha.com/varsity/module/technical-analysis/
All the patterns described in this script are based on Japanese Candlesticks.
I have only defined single candlestick patterns as of now.
(Marubozu, The spinning top, The dojis, Paper Umbrella (hammer and hanging man), Shooting star).
Currently, I am using nsetools (https://github.com/vsjha18/nsetools) for extracting real-time data from
National Stock Exchange (NSE).

### TODO
 - Integrate with Zerodha's kite api (https://kite.trade/) to execute transactions.
 - Add more visualizations.
 - Add multiple-cnadlestick patterns.
 - Add voume monitoring, technical indicators functionality.
 - Add futures and options functionality.
 - Add % change in price.
 - Set alerts for anything anomal (abnormal) for all stocks.
 - Calculate beta; refer chaper 11, module 4 of Zerodha varsity.
 - Calculate volatility; refer chaper 16, module 5 of Zerodha varsity.
 - Implement Black and Scholes option pricing model.
 
 #### Sample screenshots
 - stock_candlestick_patterns.py
<p align="center">
<img src="https://github.com/seedlit/trade-and-notify/blob/master/images/nse_patterns.png" height = "267" width = "800">
</p>
 - monitor_stocks_and_alert.py
<p align="center">
<img src="https://github.com/seedlit/trade-and-notify/blob/master/images/finnhub_apple.png" height = "317" width = "800">
</p>

Message notification.
<p align="center">
<img src="https://github.com/seedlit/trade-and-notify/blob/master/images/message_notification.jpeg" height = "200" width = "500">
</p>
