from django import forms
from trader.models import StartTrade

class StartTradeForm(forms.Form):
    class Meta:
        model = StartTrade