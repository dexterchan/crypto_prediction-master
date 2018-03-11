import requests
import time
import datetime
import os
import logging
import pathlib
import argparse
from pathlib import Path

class CoinMarketCapQuote:

    def __init__(self, mypath):
        logging.basicConfig(level=logging.DEBUG)
        self.currencyLst = ['bitcoin','ethereum','ripple','litecoin','eos','iota']
        self.extractionServiceURL="https://api.coinmarketcap.com/v1/ticker/"
        self.keys = ["price_usd","24h_volume_usd","market_cap_usd","available_supply","total_supply","percent_change_1h","percent_change_24h","percent_change_7d"]
        self.vals = [0]*(len(self.keys))

        self.path=mypath

        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        pass

    def extractCrypto(self, ccy):
        if(not Path(self.path).exists()):
            logging.error(self.path+ " not exists")
            exit(-1)
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

parser = argparse.ArgumentParser(__file__, description="Stream data")

parser.add_argument("--dataPath", "-p", dest='dataPath', help="Input a dataPath" )
args = parser.parse_args()
defaultPath="./data"
mypath=args.dataPath
if (mypath is None):
    mypath=defaultPath
mypath=mypath+"/"
quote = CoinMarketCapQuote(mypath)

while (True):
    try:
        for ccy in quote.currencyLst:
            status=quote.extractCrypto(ccy)
            logging.info(status)
        time.sleep(60)
    except :
        logging.error("Error connecting to ".format(quote.extractionServiceURL))
        time.sleep(60)
    #quote.extractCrypto("ethereum")
    #quote.extractCrypto("iota")
