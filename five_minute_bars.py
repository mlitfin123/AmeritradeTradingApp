import config, requests, json
from datetime import datetime
import asyncio
import time

while True:
    holdings = open ('data/movers.csv').readlines()

    symbols = [holding.split(',')[0].strip() for holding in holdings]
    symbols = ",".join(symbols)

    fiveminute_bars_url = config.BARS_URL + '/5Min?symbols='+ symbols

    r = requests.get(fiveminute_bars_url, headers=config.HEADERS)

    data = r.json()
    print(data)
    async def loop():
        for symbol in data:
            print(symbol)
            filename = 'data/ohlc/{}.txt'.format(symbol)
            f = open(filename, 'w+')
            f.write('Date,Open,High,Low,Close,Volume,OpenInterest\n')
            await asyncio.sleep(.1)
            for bar in data[symbol]:
                t = datetime.fromtimestamp(bar['t'])
                day = t.strftime('%Y-%m-%d-%M')

                line = '{},{},{},{},{},{},{}\n'.format(day, bar['o'], bar['h'], bar['l'], bar['c'], bar['v'], 0.00)
                f.write(line)
    asyncio.run(loop())
    time.sleep(60)