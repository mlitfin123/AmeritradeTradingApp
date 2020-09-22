from django.urls import path
from trader import views
from trader.models import StartTrade

urlpatterns = [
    path("", views.home, name="home"),
    path("trader/", views.trader, name="trader"),
]