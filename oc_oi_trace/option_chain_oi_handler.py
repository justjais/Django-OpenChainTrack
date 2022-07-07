import requests
import json
import math
import time

# Method to get nearest strikes
def round_nearest(x,num=50): return int(math.ceil(float(x)/num)*num)
def nearest_strike_bnf(x): return round_nearest(x,100)
def nearest_strike_nf(x): return round_nearest(x,50)

# Urls for fetching Data
url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)


class option_chain_oi_handler(object):
    def __init__(self):
        self.set_header()

    def get_data(self, url):
        try:
            set_cookie()
            response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
            if(response.status_code==401):
                set_cookie()
                response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
            if(response.status_code==200):
                return response.text
            return ""
        except Exception:
            pass

    def set_header(self):
        try:
            global bnf_ul
            global nf_ul
            global bnf_nearest
            global nf_nearest
            response_text = self.get_data(url_indices)
            data = json.loads(response_text)
            for index in data["data"]:
                if index["index"]=="NIFTY 50":
                    nf_ul = index["last"]
                    #print("nifty")
                if index["index"]=="NIFTY BANK":
                    bnf_ul = index["last"]
                    #print("banknifty")
            bnf_nearest=nearest_strike_bnf(bnf_ul)
            nf_nearest=nearest_strike_nf(nf_ul)
        except Exception:
            pass

    # Showing Header in structured format with Last Price and Nearest Strike

    # def print_header(index="",ul=0,nearest=0):
    #     print(strPurple( index.ljust(12," ") + " => ")+ strLightPurple(" Last Price: ") + strBold(str(ul)) + strLightPurple(" Nearest Strike: ") + strBold(str(nearest)))

    # def print_hr():
    #     print(strYellow("|".rjust(70,"-")))

    # Fetching CE and PE data based on Nearest Expiry Date
    def print_oi(self, num,step,nearest,url):
        try:
            strike = nearest - (step*num)
            start_strike = nearest - (step*num)
            response_text = self.get_data(url)
            data = json.loads(response_text)
            currExpiryDate = data["records"]["expiryDates"][0]
            for item in data['records']['data']:
                if item["expiryDate"] == currExpiryDate:
                    if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                        #print(strCyan(str(item["strikePrice"])) + strGreen(" CE ") + "[ " + strBold(str(item["CE"]["openInterest"]).rjust(10," ")) + " ]" + strRed(" PE ")+"[ " + strBold(str(item["PE"]["openInterest"]).rjust(10," ")) + " ]")
                        print(data["records"]["expiryDates"][0] + " " + str(item["strikePrice"]) + " CE " + "[ " + strBold(str(item["CE"]["changeinOpenInterest"]).rjust(10," ")) + " ]" + " PE " + "[ " + strBold(str(item["PE"]["changeinOpenInterest"]).rjust(10," ")) + " ]")
                        strike = strike + step
        except Exception:
            pass

    # Finding highest Open Interest of People's in CE based on CE data
    def highest_oi_CE(self, num,step,nearest,url):
        try:
            strike = nearest - (step*num)
            start_strike = nearest - (step*num)
            response_text = self.get_data(url)
            data = json.loads(response_text)
            currExpiryDate = data["records"]["expiryDates"][0]
            max_oi = 0
            max_oi_strike = 0
            total_CE_OI = 0
            for item in data['records']['data']:
                if item["expiryDate"] == currExpiryDate:
                    if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                        if item["CE"]["openInterest"] > max_oi:
                            max_oi = item["CE"]["openInterest"]
                            max_oi_strike = item["strikePrice"]
                        total_CE_OI += item["CE"]["changeinOpenInterest"]
                        strike = strike + step
            return max_oi_strike, total_CE_OI
        except Exception:
            return None, None

    # Finding highest Open Interest of People's in PE based on PE data
    def highest_oi_PE(self, num,step,nearest,url):
        try:
            strike = nearest - (step*num)
            start_strike = nearest - (step*num)
            response_text = self.get_data(url)
            data = json.loads(response_text)
            currExpiryDate = data["records"]["expiryDates"][0]
            max_oi = 0
            max_oi_strike = 0
            total_PE_OI = 0
            for item in data['records']['data']:
                if item["expiryDate"] == currExpiryDate:
                    if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                        if item["PE"]["openInterest"] > max_oi:
                            max_oi = item["PE"]["openInterest"]
                            max_oi_strike = item["strikePrice"]
                        total_PE_OI += item["PE"]["changeinOpenInterest"]
                        strike = strike + step
            return max_oi_strike, total_PE_OI
        except Exception:
            return None, None


    NF_PCR = []
    BNF_PCR = []
    #while True:
    
    # print('\033c')
    # print_hr()
    # print_header("Nifty",nf_ul,nf_nearest)
    # print_hr()
    # print_oi(10,50,nf_nearest,url_nf)

    # print_hr()
    # print_oi(10,100,bnf_nearest,url_bnf)

    def nifty_oc_oi_ce_data(self):
        try:
            # self.set_header()
            # Finding Highest OI in Call Option In Nifty
            nf_highestoi_CE, nf_total_CE_OI = self.highest_oi_CE(10,50,nf_nearest,url_nf)
            return nf_highestoi_CE, nf_total_CE_OI
        except Exception:
            time.sleep(60)
    
    def nifty_oc_oi_pe_data(self):
        try:
            # Finding Highet OI in Put Option In Nifty
            nf_highestoi_PE, nf_total_PE_OI = self.highest_oi_PE(10,50,nf_nearest,url_nf)
            return nf_highestoi_PE, nf_total_PE_OI
        except Exception:
            time.sleep(60)

    def banknifty_oc_oi_ce_data(self):
        try:
            # Finding Highest OI in Call Option In Bank Nifty
            bnf_highestoi_CE, bnf_total_CE_OI = self.highest_oi_CE(10,100,bnf_nearest,url_bnf)
            return bnf_highestoi_CE, bnf_total_CE_OI
        except Exception:
            time.sleep(60)

    def banknifty_oc_oi_pe_data(self):
        try:
            # Finding Highest OI in Put Option In Bank Nifty
            bnf_highestoi_PE, bnf_total_PE_OI = self.highest_oi_PE(10,100,bnf_nearest,url_bnf)
            return bnf_highestoi_PE, bnf_total_PE_OI
        except Exception:
            time.sleep(60)


    def set_data(self):
        #while True:
        try:
            # Finding Highest OI in Call Option In Nifty
            nf_highestoi_CE, nf_total_CE_OI = self.highest_oi_CE(10,50,nf_nearest,url_nf)

            # Finding Highet OI in Put Option In Nifty
            nf_highestoi_PE, nf_total_PE_OI = self.highest_oi_PE(10,50,nf_nearest,url_nf)

            # Finding Highest OI in Call Option In Bank Nifty
            bnf_highestoi_CE, bnf_total_CE_OI = self.highest_oi_CE(10,100,bnf_nearest,url_bnf)

            # Finding Highest OI in Put Option In Bank Nifty
            bnf_highestoi_PE, bnf_total_PE_OI = self.highest_oi_PE(10,100,bnf_nearest,url_bnf)

            # print_hr()
            # print(strCyan(str("Major Support in Nifty: ")) + str(nf_highestoi_CE))
            # print(strCyan(str("Major Resistance in Nifty: ")) + str(nf_highestoi_PE))
            # print(strCyan(str("TOTAL Change in CE OI in Nifty: ")) + str(nf_total_CE_OI))
            # print(strCyan(str("TOTAL Change in PE OI in Nifty: ")) + str(nf_total_PE_OI))
            #NF_PCR = round(nf_total_PE_OI/nf_total_CE_OI, 2)
            if nf_total_CE_OI != 0:
                diff_pcr = [round(nf_total_PE_OI / nf_total_CE_OI, 2)]
            else:
                diff_pcr = [0]
            diff_pcr.extend(NF_PCR)
            NF_PCR = diff_pcr
            #NF_PCR.append(diff_pcr)
            #NF_PCR = NF_PCR[::-1]
            #print(strCyan(str("Diff PCR for Nifty: ")) + str(diff_pcr[:10]))
            if NF_PCR[0] >= 1:
                pass
                #print(strCyan(str("Signal: ")) + strGreen(str("BUY/CE")))
            else:
                pass
                #print(strCyan(str("Signal: ")) + strRed(str("SELL/PE")))
            # print_hr()
            # print_header("Bank Nifty",bnf_ul,bnf_nearest)
            # print_hr()
            # print(strPurple(str("Major Support in Bank Nifty:")) + str(bnf_highestoi_CE))
            # print(strPurple(str("Major Resistance in Bank Nifty:")) + str(bnf_highestoi_PE))
            # print(strPurple(str("TOTAL Change in CE OI in BankNifty: ")) + str(bnf_total_CE_OI))
            # print(strPurple(str("TOTAL Change in PE OI in BankNifty: ")) + str(bnf_total_PE_OI))
            # BNF_PCR = round(bnf_total_PE_OI/bnf_total_CE_OI, 2)
            if bnf_total_CE_OI != 0:
                diff_pcr = [round(bnf_total_PE_OI / bnf_total_CE_OI, 2)]
            else:
                diff_pcr = [0]
            diff_pcr.extend(BNF_PCR)
            BNF_PCR = diff_pcr
            #BNF_PCR.append(diff_pcr)
            #BNF_PCR = BNF_PCR[::-1]
            #print(strPurple(str("Diff PCR for BankNifty: ")) + str(diff_pcr[:10]))
            if BNF_PCR[0] >= 1:
                pass
                #print(strCyan(str("Signal: ")) + strGreen(str("BUY/CE")))
            else:
                pass
                #print(strCyan(str("Signal: ")) + strRed(str("SELL/PE")))
            #print_hr()
            return nf_highestoi_CE, nf_total_CE_OI
            #time.sleep(240)
        except Exception:
            time.sleep(60)