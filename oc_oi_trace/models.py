from django.db import models
from django.contrib.auth.models import User


SYMBOL_CHOICES = (
    ('nifty','NIFTY'),
    ('banknifty', 'BANKNIFTY'),
)

class OptionChainData(models.Model):
    timestamp = models.TimeField(auto_now=False, auto_now_add=False)
    option_chain_symbol = models.CharField(max_length=10, choices=SYMBOL_CHOICES)
    total_CE_OI = models.CharField(max_length=10)
    total_PE_OI = models.CharField(max_length=10)
    diff = models.CharField(max_length=10)
    diff_pcr = models.CharField(max_length=10)
    signal = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.option_chain_symbol + str(self.timestamp)
