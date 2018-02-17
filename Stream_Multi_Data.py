import requests
import time
import datetime
import os
import logging
import pathlib



class CoinMarketCapQuote:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.currencyLst = ['bitcoin','ethereum','ripple','litecoin','eos','iota']
        self.extractionServiceURL="https://api.coinmarketcap.com/v1/ticker/"
        self.keys = ["price_usd","24h_volume_usd","market_cap_usd","available_supply","total_supply","percent_change_1h","percent_change_24h","percent_change_7d"]
        self.vals = [0]*(len(self.keys))

        self.path="data/"

        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        pass

    def extractCrypto(self, ccy):
        f_name=self.path+"live.mkt."+ccy+".csv"
        f = open(f_name,"a")
        url = self.extractionServiceURL+ccy
        data = requests.get(url).json()[0]


        for d in data.keys():
            if d in self.keys:
                indx = self.keys.index(d)
                self.vals[indx] = data[d]
        for val in self.vals:
            f.write(val+",")
        timenow = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        f.write(","+timenow)
        f.write("\n")
        f.flush()
        logging.debug(ccy+":"+str(self.vals)+timenow)
        return ccy+":"+str(self.vals)+timenow



quote = CoinMarketCapQuote()

while (True):
    for ccy in quote.currencyLst:
        status=quote.extractCrypto(ccy)
        logging.info(status)
    time.sleep(60)
    #quote.extractCrypto("ethereum")
    #quote.extractCrypto("iota")
