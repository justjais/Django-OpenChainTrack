from datetime import datetime
import re
from zoneinfo import ZoneInfo
from django.shortcuts import render
from .option_chain_oi_handler import option_chain_oi_handler
from .models import OptionChainData
from .forms import OC_OI_FORM


IN = ZoneInfo("Asia/Kolkata")

def home(request):
    return render(request, 'oc_oi_trace/home.html')

def option_chain_oi(request):
    oi_obj = option_chain_oi_handler()
    nf_highestoi_CE, nf_total_CE_OI = oi_obj.nifty_oc_oi_ce_data()
    nf_highestoi_PE, nf_total_PE_OI = oi_obj.nifty_oc_oi_pe_data()
    nf_total_pe_ce_diff = nf_total_PE_OI - nf_total_CE_OI
    nf_diff_pcr_val = get_pcr_value(nf_total_PE_OI, nf_total_CE_OI)
    if nf_diff_pcr_val >= 1:
        nf_signal = True
    else:
        nf_signal = False
    new_nf_entry = OptionChainData(
        timestamp=datetime.now(IN).strftime('%H:%M:%S'),
        option_chain_symbol='nifty',
        total_CE_OI=nf_total_CE_OI,
        total_PE_OI=nf_total_PE_OI,
        diff=nf_total_PE_OI - nf_total_CE_OI,
        diff_pcr=nf_diff_pcr_val,
        signal=nf_signal
    )
    new_nf_entry.save()
    
    bnf_highestoi_CE, bnf_total_CE_OI = oi_obj.banknifty_oc_oi_ce_data()
    bnf_highestoi_PE, bnf_total_PE_OI = oi_obj.banknifty_oc_oi_pe_data()
    bnf_total_pe_ce_diff = bnf_total_PE_OI - bnf_total_CE_OI
    bnf_diff_pcr_val = get_pcr_value(bnf_total_PE_OI, bnf_total_CE_OI)
    if bnf_diff_pcr_val >= 1:
        bnf_signal = True
    else:
        bnf_signal = False
    new_bnf_entry = OptionChainData(
        timestamp=datetime.now(IN).strftime('%H:%M:%S'),
        option_chain_symbol='banknifty',
        total_CE_OI=bnf_total_CE_OI,
        total_PE_OI=bnf_total_PE_OI,
        diff=bnf_total_PE_OI - bnf_total_CE_OI,
        diff_pcr=bnf_diff_pcr_val,
        signal=bnf_signal
    )
    new_bnf_entry.save()

    oc_oi_objs = OptionChainData.objects.all()
    return render(
        request, 
        'oc_oi_trace/option_chain_oi.html',
        {
            'oc_oi_objs': oc_oi_objs,
            'nifty': request.GET.get('nifty'),
            'banknifty': request.GET.get('banknifty'),
        }
    )

    return render(
        request, 'oc_oi_trace/option_chain_oi.html', 
        {
            'nifty': request.GET.get('nifty'),
            'banknifty': request.GET.get('banknifty'),
            'date_time': datetime.now(IN).strftime('%Y-%m-%d %H:%M:%S'),
            'nf_major_support': nf_highestoi_CE,
            'nf_major_resistance': nf_highestoi_PE,
            'nf_total_CE_OI': nf_total_CE_OI,
            'nf_total_PE_OI': nf_total_PE_OI,
            'nf_diff': nf_total_pe_ce_diff,
            'nf_diff_PCR': nf_diff_pcr_val,
            'nf_signal': nf_signal,
            'bnf_major_support': bnf_highestoi_CE,
            'bnf_major_resistance': bnf_highestoi_PE,
            'bnf_total_CE_OI': bnf_total_CE_OI,
            'bnf_total_PE_OI': bnf_total_PE_OI,
            'bnf_diff': bnf_total_pe_ce_diff,
            'bnf_diff_PCR': bnf_diff_pcr_val,
            'bnf_signal': bnf_signal,
        }
    )

def get_pcr_value(total_PE_OI, total_CE_OI):
    if total_CE_OI != 0:
        diff_pcr = round(total_PE_OI / total_CE_OI, 2)
    else:
        diff_pcr = 0
    return diff_pcr
    #diff_pcr.extend(NF_PCR)
    #NF_PCR = diff_pcr
