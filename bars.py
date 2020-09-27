import config, requests, json
from datetime import datetime
import time

while True:
    holdings = open ('data/qqq.csv').readlines()

    symbols = [holding.split(',')[2].strip() for holding in holdings][1:]
    symbols = ",".join(symbols)

    # oneminute_bars_url = config.BARS_URL + '/1Min?symbols='+ symbols
    fiveminute_bars_url = config.BARS_URL + '/5Min?symbols='+ symbols
    # day_bars_url = '{}/day?symbols={}&limit=1000'.format(config.BARS_URL, symbols)

    # r = requests.get(fiveminute_bars_url, headers=config.HEADERS)
    r = requests.get(fiveminute_bars_url, headers=config.HEADERS)
    # r = requests.get(day_bars_url, headers=config.HEADERS)

    data = r.json()

    for symbol in data:
        filename = 'data/ohlc/{}.txt'.format(symbol)
        f = open(filename, 'w+')
        f.write('Date,Open,High,Low,Close,Volume,OpenInterest\n')
        for bar in data[symbol]:
            t = datetime.fromtimestamp(bar['t'])
            day = t.strftime('%Y-%m-%d-%M')

            line = '{},{},{},{},{},{},{}\n'.format(day, bar['o'], bar['h'], bar['l'], bar['c'], bar['v'], 0.00)
            f.write(line)
    time.sleep(60)