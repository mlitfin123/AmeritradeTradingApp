from django.urls import path
from trader import views
from trader.models import StartTrade

urlpatterns = [
    path("", views.home, name="home"),
    path("trader/", views.trader, name="trader"),
    path("tradefivescript/", views.startFiveScript, name="tradefivescript"),
    path("trademinscript/", views.startMinScript, name="trademinscript"),
    path("trademinbarscript/", views.startMinBars, name="trademinbarscript"),
    path("tradefivebarscript/", views.startFiveBars, name="tradefivebarscript")
]