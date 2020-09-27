import json, requests, sys
import btalib
import pandas as pd
from datetime import datetime
from config import ALPACA_KEY, ALPACA_SECRET
import time

while True:

    in_position = False
    SYMBOL = 'CBAT'
    BASE_URL = "https://paper-api.alpaca.markets"
    ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
    ORDERS_URL = "{}/v2/orders".format(BASE_URL)
    POSITIONS_URL = "{}/v2/positions/{}".format(BASE_URL, SYMBOL)

    HEADERS = {'APCA-API-KEY-ID': ALPACA_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET}

    def place_order():
        data = {
            "symbol": SYMBOL,
            "qty": 50,
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",
        }

        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

        response = json.loads(r.content)

        print(response)

    def close_position():
        data = {
            "symbol": SYMBOL,
            "qty": 50,
            "side": "sell",
            "type": "market",
            "time_in_force": "gtc",
        }

        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

        response = json.loads(r.content)

        print(response)

    # Read a csv file into a pandas dataframe
    df = pd.read_csv('data/ohlc/CBAT.txt', parse_dates=True, index_col='Date')
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
    df.rsi.to_csv('data/technicals/rsi.csv', header=True, index=False)
    df.macd.to_csv('data/technicals/macd.csv', header=True, index=False)
    df.signal.to_csv('data/technicals/signal.csv', header=True, index=False)

    readRSI = open ('data/technicals/rsi.csv').readlines()
    readMACD = open ('data/technicals/macd.csv').readlines()
    readSignal = open ('data/technicals/signal.csv').readlines()

    newRSI= float(readRSI[100].rstrip("\n"))
    newMACD= float(readMACD[100].rstrip("\n"))
    newSignal= float(readSignal[100].rstrip("\n"))
    print(newRSI)
    print(newMACD)
    print(newSignal)
    if newRSI < 30:
        print('Oversold!')
        if not in_position:
            print("== Placing order and setting in position to true ==")
            in_position = True
            place_order()

    if newRSI > 70:
        print('Overbought!')
        if in_position:
            print("== Closing position and setting in position to false ==")
            in_position = False
            close_position()

    if newMACD > newSignal:
        print('MACD Buy Signal!')
        if not in_position:
            print("== Placing order and setting in position to true ==")
            in_position = True
            place_order()
    
    if newMACD < newSignal:
        print('MACD Sell Signal!')
        if in_position:
            print("== Closing position and setting in position to false ==")
            in_position = False
            place_order()

    time.sleep(60)