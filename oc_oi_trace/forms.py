from dataclasses import fields
from django.forms import ModelForm
from .models import OptionChainData

class OC_OI_FORM(ModelForm):
    class Meta:
        model = OptionChainData
        fields = ['timestamp', 'option_chain_symbol', 'total_CE_OI', 'total_PE_OI', 'diff', 'diff_pcr', 'signal']
