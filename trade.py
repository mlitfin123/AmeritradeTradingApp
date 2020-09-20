from tda import auth, client
from tda.client import Client
from tda.orders.common import OrderType, Session, Duration
from tda.orders.equities import equity_buy_market, equity_buy_limit
from tda.orders.generic import OrderBuilder

import json
import config

try:
    c = auth.client_from_token_file(config.TOKEN_PATH, config.API_KEY)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path=config.CHROMEDRIVER_PATH) as driver:
        c = auth.client_from_login_flow(
            driver, config.API_KEY, config.REDIRECT_URI, config.TOKEN_PATH)

builder = equity_buy_limit("REKR", 2, 2)

res = c.place_order(config.ACCOUNT_ID, builder.build())

print(res)