import json, requests, sys
import btalib
import pandas as pd
from datetime import datetime
import alpaca_trade_api as tradeapi
from config import ALPACA_KEY, ALPACA_SECRET
import time
import logging

in_position = False

while True:
    holdings = open ('data/minute_movers.csv').readlines()
    BASE_URL = "https://paper-api.alpaca.markets"
    api = tradeapi.REST(ALPACA_KEY, ALPACA_SECRET, base_url=BASE_URL) # or use ENV Vars shown below
    account = api.get_account()
    clock = api.get_clock()

    for symbol in holdings:
        SYMBOL = symbol.rstrip("\n")
        print(SYMBOL)

        def place_order():
            api.submit_order(
                symbol=SYMBOL,
                qty="50",
                side="buy",
                type="market",
                time_in_force="gtc",
            )

        def close_position():
            print(SYMBOL)
            api.close_position(
                symbol=SYMBOL
            )
            
        try:
            api.get_position(SYMBOL)
            in_position = True
            print (in_position)
        except Exception as e:
            logging.error(e)
            in_position = False
            print (in_position)

        # Read a csv file into a pandas dataframe
        df = pd.read_csv('data/ohlc/'+ SYMBOL +'.txt', parse_dates=True, index_col='Date')
        sma = btalib.sma(df)

        sma = btalib.sma(df)
        rsi = btalib.rsi(df)

        df['sma'] = sma.df
        df['rsi'] = rsi.df

        macd = btalib.macd(df)

        df['macd'] = macd.df['macd']
        df['signal'] = macd.df['signal']
        df['histogram'] = macd.df['histogram']
        print(df)
        df.rsi.to_csv('data/technicals/'+ SYMBOL +'rsi.csv', header=True, index=False)
        df.macd.to_csv('data/technicals/'+ SYMBOL +'macd.csv', header=True, index=False)
        df.signal.to_csv('data/technicals/'+ SYMBOL +'signal.csv', header=True, index=False)

        readRSI = open ('data/technicals/'+ SYMBOL +'rsi.csv').readlines()
        readMACD = open ('data/technicals/'+ SYMBOL +'macd.csv').readlines()
        readSignal = open ('data/technicals/'+ SYMBOL +'signal.csv').readlines()

        newRSI= float(readRSI[100].rstrip("\n"))
        newMACD= float(readMACD[100].rstrip("\n"))
        newSignal= float(readSignal[100].rstrip("\n"))
        print(newRSI)
        print(newMACD)
        print(newSignal)

        print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
        if clock.is_open and newRSI < 30:
            print('Oversold!')
            if in_position == False:
                print("== Placing order ==")
                place_order()

        if clock.is_open and newRSI > 70:
            print('Overbought!')
            if in_position == True:
                print("== Closing position ==")
                close_position()

        if clock.is_open and newMACD > newSignal:
            print('MACD Buy Signal!')
            if in_position == False and newRSI < 60:
                print("== Placing order ==")
                place_order()
        
        if newMACD < newSignal:
            print('MACD Sell Signal!')
            if in_position == True and newRSI > 30:
                print("== Closing position ==")
                close_position()

    time.sleep(60)