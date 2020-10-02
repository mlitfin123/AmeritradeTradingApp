from django.shortcuts import render
from django.shortcuts import render
import re
import os
from django.http import HttpResponse
from django.shortcuts import redirect
from trader.forms import StartTradeForm
from trader.models import StartTrade
from django.views.generic import ListView
from tda import auth, client
from tda.client import Client
from tda.orders.common import OrderType, Session, Duration
from tda.orders.equities import equity_buy_market, equity_buy_limit
from tda.orders.generic import OrderBuilder

import json
import config
# authenticates the client
try:
    c = auth.client_from_token_file(config.TOKEN_PATH, config.API_KEY)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path=config.CHROMEDRIVER_PATH) as driver:
        c = auth.client_from_login_flow(
            driver, config.API_KEY, config.REDIRECT_URI, config.TOKEN_PATH)
# performs the trade
def trader(request):
    form = StartTradeForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            builder = equity_buy_limit("REKR", 2, 2)
            res = c.place_order(config.ACCOUNT_ID, builder.build())
            print(res)
            return redirect("home")
    else:
        print('failed')
        return render(request, "trader/start_trade.html", {"form": form})

def startFiveBars(request):
    if request.method == "POST":
        import five_minute_bars
        print('scriptstarted')
    else:
        print('failedScript')
        return render(request, "trader/five_min_trade.html")

def startFiveScript(request):
    if request.method == "POST":
        import minute_bars
        print('scriptstarted')
    else:
        print('failedScript')
        return render(request, "trader/five_min_trade.html")

def startMinBars(request):
    if request.method == "POST":
        import minuteTA
        print('scriptstarted')
    else:
        print('failedScript')
        return render(request, "trader/one_min_trade.html")

def startMinScript(request):
    if request.method == "POST":
        import minuteTA
        print('scriptstarted')
    else:
        print('failedScript')
        return render(request, "trader/one_min_trade.html")

def home(request):
    return render(request, "trader/home.html")