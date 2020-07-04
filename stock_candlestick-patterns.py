"""
Author: Naman Jain
Email: naman.jain@btech2015.iitgn.ac.in
       www.namanji.wixsite.com/naman/

The aim of writing this script is to minimize my need to look at stock prices multiple times a day.
Rather these functions should be able to montior the stock prices and notify me if I should make a trading decision

The patterns defined in this script are inspired from Zerodha's Varstity Module 2, 'Technical Analysis'.
Here is the link to the module - https://zerodha.com/varsity/module/technical-analysis/
All the patterns described in this script are based on Japanese Candlesticks.
I have only defined single candlestick patterns as of now.
(Marubozu, The spinning top, The dojis, Paper Umbrella (hammer and hanging man), Shooting star)

Currently, I am using nsetools (https://github.com/vsjha18/nsetools) for extracting real-time data from
National Stock Exchange (NSE).
"""
#------------------------------------------------------------------------------------------

# TODO: Add visualizations functionality.
#       Define Multiplecandlestick patterns
#       Add functionality to send notifications.

from nsetools import Nse
import time
from multiprocessing import Pool, Manager

def get_stock_variables(stock_symbol, global_list):           
    stock_variables = Nse().get_quote(stock_symbol)      
    global_list.append(stock_variables)

    
def marubozu(stock_variables, threshold = 0.5, body_range = [1,10]):
    """
    stock_variables: {dict} A dictionary containing all the useful values (open, high, etc.)
    threshold: {float} Threshold in % for the lenght of shadows (head and tail)
    body_range: {list} Range in % within which the length of real body must lie.

    Marubozu is a candlestick which only consists of body. It does not have any head or tail, or if it does they are very small.
    Bullish Marubozu: Open~Low; Close~High; Head = (High-Close)~0; Tail = (Open-Low)~0
                      Bullish Marubozu indicates that there is so much interest in buying the stock that participants are willing to buy
                      at any available price. One should buy (long) in this case. Stop Loss = Low.
    Bearish Marubozu: Open~High; Close~Low; Head = (High-Open)~0; Tail = (Close-Low)~0
                      It indicates that there is so much selling pressure in the market that participants are willing to sell at any avialable price.
                      On should short in such case. Stop loss = High
    """    
    try: 
        stock_symbol = stock_variables['symbol']          
        current_price = stock_variables['lastPrice']
        open_price = stock_variables['open']
        low_price = stock_variables['dayLow']
        high_price = stock_variables['dayHigh']
        if current_price >= open_price:     # bullish
            head = high_price - current_price
            tail = open_price - low_price
            body = (current_price - open_price)/open_price
            if (head / high_price)*100 <= threshold and (tail / low_price)*100 <= threshold and body >= body_range[0] and body <= body_range[1]:
                print('Fuck yeah, it is BULLISH Marubozu. Go long on {} you nutcase!'.format(stock_symbol))
                print('Remeber, the stop loss trigger is ', low_price)
                return True            
        elif current_price < open_price:   # bearish
            head = high_price - open_price
            tail = current_price - low_price
            body = (open_price - current_price)/current_price
            if (head / high_price)*100 <= threshold and (tail / low_price)*100 <= threshold and body >= body_range[0] and body <= body_range[1]:
                print('Fuck yeah, it is BEARISH Marubozu. Go short on {} you nutcase!'.format(stock_symbol))
                print('Remember, the stop loss trigger is ', high_price)
                return True            
    except Exception as e:
        print('some exception in {}: {}'.format(stock_symbol, e))


def spinning_top(stock_variables, body_threshold = 2, shadow_factor = 2):
    """
    stock_variables: {dict} A dictionary containing all the useful values (open, high, etc.)
    body_threshold: {float} Threshold in % for the length of the real body
    shadow_factor: {float} Minimum length of each shadow = shadow_factor * real body

    Spinning Top has a small real body; head and tail are almost equal. Can be bull or bear.
    It shows confusion and indecision in the market with an equal probability of reversal and continuation. 
    More sideways movement can also follow.
    Think of it as the 'Calm before the Storm'. Should decide on 50% of stock.
    """
    try:
        stock_symbol = stock_variables['symbol']          
        current_price = stock_variables['lastPrice']
        open_price = stock_variables['open']
        low_price = stock_variables['dayLow']
        high_price = stock_variables['dayHigh'] 
        if current_price >= open_price:     # bullish
            head = high_price - open_price
            tail = open_price - low_price
            body = current_price - open_price
            if (body/open_price)*100 <= body_threshold and (head/body) >= shadow_factor and (tail/body) >= shadow_factor: #TODO: Update logic for shadows. Head and tail must be of similar lengths.
                print('{}: It is Bullish SPINNING TOP. Be prepared. A storm might be coming!'.format(stock_symbol))
                print('Remeber, good idea is to trade on 50 percent stock')
                return True            
        elif current_price < open_price:     # bearish
            head = high_price - current_price
            tail = current_price - low_price
            body = open_price - current_price
            if (body/current_price)*100 <= body_threshold and (head/body) >= shadow_factor and (tail/body) >= shadow_factor: #TODO: Update logic for shadows. Head and tail must be of similar lengths.
                print('{}: It is Bearish SPINNING TOP. Be prepared. A storm might be coming!'.format(stock_symbol))
                print('Remeber, good idea is to trade on 50 percent stock')
                return True            
    except Exception as e:
        print('some exception in {}: {}'.format(stock_symbol, e))

    
def doji(stock_variables, body_threshold = 0.5, shadow_factor = 4):
    """
    stock_variables: {dict} A dictionary containing all the useful values (open, high, etc.)
    body_threshold: {float} Threshold in % for the length of the real body
    shadow_factor: {float} Minimum length of each shadow = shadow_factor * real body

    A doji is similar to spinning top, except that it does not have a real body. Can be bull or bear.
    It can occur individually or in cluster.
    It shows confusion and indecision in the market with an equal probability of reversal and continuation. 
    More sideways movement can also follow.
    Think of it as the 'Calm before the Storm'. Should decide on 50% of stock.
    """
    try:
        stock_symbol = stock_variables['symbol']          
        current_price = stock_variables['lastPrice']
        open_price = stock_variables['open']
        low_price = stock_variables['dayLow']
        high_price = stock_variables['dayHigh'] 
        if current_price >= open_price:     # bullish
            head = high_price - open_price
            tail = open_price - low_price
            body = current_price - open_price
            if (body/open_price)*100 <= body_threshold and (head/body) >= shadow_factor and (tail/body) >= shadow_factor: #TODO: Update logic for shadows. Head and tail must be of similar lengths.
                print('{}: It is Bullish DOJI. Be prepared. A storm might be coming!'.format(stock_symbol))
                print('Remeber, good idea is to trade on 50 percent stock')
                return True            
        elif current_price < open_price:     # bearish
            head = high_price - current_price
            tail = current_price - low_price
            body = open_price - current_price
            if (body/current_price)*100 <= body_threshold and (head/body) >= shadow_factor and (tail/body) >= shadow_factor: #TODO: Update logic for shadows. Head and tail must be of similar lengths.
                print('{}: It is Bearish DOJI. Be prepared. A storm might be coming!'.format(stock_symbol))
                print('Remeber, good idea is to trade on 50 percent stock')
                return True            
    except Exception as e:
        print('some exception in {}: {}'.format(stock_symbol, e))


def paper_umbrella(stock_variables, body_range = [0,2], tail_factor = 2, head_factor = 0.5):
    """
    stock_variables: {dict} A dictionary containing all the useful values (open, high, etc.)   
    tail_factor: {float} Minimum length of tail shadow = tail_factor * real body
    head_factor: {float} length of head shadow <= head_factor * tail shadow length 
                 (Computing in terms of tail shadow so that we don't miss this pattern in case of non existent real body)

    There are two types of paper umbrella: Hammer, and the Hanging Man. Both are essentially same but their prior trend differ.
    Both suggest that the current trend may change.
    For hammer, the prior trend should be downwards (bearish). For hanging man, it should be upwards (bullish).
    It can be bullish or bearish. It is better if hammer is bullish and hanging man is bearish. But doesn't matter much.
    Conditions:
            The (length of tail / length of real body) >= 2
            Open and close should be almost the same (within 1-2% range)
            Little to non-existent head shadow.
    It is advisble to follow hammer more than hanging man.
    """
    try:
        stock_symbol = stock_variables['symbol']          
        current_price = stock_variables['lastPrice']
        open_price = stock_variables['open']
        low_price = stock_variables['dayLow']
        high_price = stock_variables['dayHigh'] 
        if current_price >= open_price:     # bullish
            head = high_price - open_price
            tail = open_price - low_price
            body = current_price - open_price
            if (body/open_price) >= body_range[0] and (body/open_price) <= body_range[1] and tail >= tail_factor*body and head <= head_factor*tail:
                print('{}: It may be Bullish HAMMER or HANGING MAN. Check prior trend.'.format(stock_symbol))
                print('Go long or short depending on prior trend. Stop Loss for long = {}; Stop Loss for short = {}'.format(low_price, high_price))
                return True            
        if current_price < open_price:     # bearish
            head = high_price - current_price
            tail = current_price - low_price
            body = open_price - current_price
            if (body/current_price) >= body_range[0] and (body/current_price) <= body_range[1] and tail >= tail_factor*body and head <= head_factor*tail:
                print('{}: It may be Bearish HAMMER or HANGING MAN. Check prior trend.'.format(stock_symbol))
                print('Go long or short depending on prior trend. Stop Loss for long = {}; Stop Loss for short = {}'.format(low_price, high_price))
                return True            
    except Exception as e:
        print('some exception in {}: {}'.format(stock_symbol, e))

def shooting_star(stock_variables, body_range = [0,2], tail_factor = 0.5, head_factor = 2):
    """
    stock_variables: {dict} A dictionary containing all the useful values (open, high, etc.)   
    head_factor: {float} Minimum length of head shadow = head_factor * real body
    tail_factor: {float} length of tail shadow <= tail_factor * head shadow length 
                 (Computing in terms of head shadow so that we don't miss this pattern in case of non existent real body)

    This is opposite to the hammer.    
    The prior trend should be upwards (bullish).    
    Conditions:
            The (length of head / length of real body) >= 2
            Open and close should be almost the same (within 1-2% range)
            Little to non-existent tail shadow.    
    """
    try:
        stock_symbol = stock_variables['symbol']          
        current_price = stock_variables['lastPrice']
        open_price = stock_variables['open']
        low_price = stock_variables['dayLow']
        high_price = stock_variables['dayHigh'] 
        if current_price >= open_price:     # bullish
            head = high_price - open_price
            tail = open_price - low_price
            body = current_price - open_price
            if (body/open_price) >= body_range[0] and (body/open_price) <= body_range[1] and tail <= tail_factor*head and head >= head_factor*body:
                print('{}: It may be Bullish SHOOTING STAR. Check prior trend.'.format(stock_symbol))
                print('Go short if prior trend is bullish. Stop Loss = {}, current price = {}'.format(high_price, current_price))
                return True            
        if current_price < open_price:     # bearish
            head = high_price - current_price
            tail = current_price - low_price
            body = open_price - current_price
            if (body/current_price) >= body_range[0] and (body/current_price) <= body_range[1] and tail <= tail_factor*head and head >= head_factor*body:
                print('{}: It may be Bearish SHOOTING STAR. Check prior trend.'.format(stock_symbol))
                print('Go short if prior trend is bullish. Stop Loss = {}, current price = {}'.format(high_price, current_price))
                return True            
    except Exception as e:
        print('some exception in {}: {}'.format(stock_symbol, e))

#---------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    while True:
        global_time_start = time.time()    
        stock_list = ['AJANTPHARM','HEROMOTOCO','INDUSINDBK','LT','MARUTI','OIL','ONGC','SBICARD','SBIN','TCS','YESBANK','BORORENEW','IRCTC']
        global_list = Manager().list()  # global variable list that will contain details for all stocks. Initiating with Manager to handle multiprocessing
        task_list = []
        for stock_symbol in stock_list:
            task_list.append([stock_symbol, global_list])
        p = Pool(len(stock_list))
        p.starmap(get_stock_variables, task_list)
        p.close()
        p.join()
        global_time_end = time.time()    
        print('global time taken ', global_time_end - global_time_start)
        
        for i in global_list:
            print(i['symbol'], i['lastPrice'])        
        for i in global_list:
            marubozu(i)
            spinning_top(i)
            doji(i)
            paper_umbrella(i)
            shooting_star(i)
