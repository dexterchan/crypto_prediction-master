import csv
import tweepy
import numpy as np
from textblob import TextBlob
import datetime
import time
import logging
import pathlib
import argparse
from pathlib import Path

class TweeterSentimentAnalyzer:
    def __init__(self, mypath):
        logging.basicConfig(level=logging.DEBUG)

        self.currencyLst = ['bitcoin','ethereum','ripple','litecoin','eos','iota']
        # set twitter api credentials
        self.consumer_key= 'JbZWz1hekxkCv1sCRW6k9BrjF'
        self.consumer_secret= 'tjZclsG6BqdGNfnUAt1wAFRzBX3PXHDGp6z54jKryVHJN3wWOo'
        self.access_token='926643380-mTGIw7bfYqF6sxbiZqNZb0LCdBypqAtIEC4rPtll'
        self.access_token_secret='4hetDuuv5lDtzzAPzyN1E1a5XX41bJeQNATggb0Mwqf3m'

        #self.path="data/"
        self.path=mypath
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)



        # access twitter api via tweepy methods
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.twitter_api = tweepy.API(auth)
        pass


    def readSentimentByTextBlob(self, ccy):
        if(not Path(self.path).exists()):
            logging.error(self.path+ " not exists")
            exit(-1)
        path = self.path+'live.tweet.'+ccy+'.csv'
        f = open(path,"a")

        # fetch tweets by keywords
        tweets = self.twitter_api.search(q=[ccy+', price, crypto'], count=100)

        # get polarity
        polarity = self.get_TextBlob_polarity(ccy,tweets)
        sentiment = np.mean(polarity)

        # save sentiment data to csv file
        f.write(str(sentiment))
        f.write(","+datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
        f.write("\n")
        f.flush()

        pass

    def get_TextBlob_polarity(self,ccy,tweets):
        # run polarity analysis on tweets
        f1 = open(self.path+"tweet_data."+ccy+'.txt','a')
        tweet_polarity = []

        for tweet in tweets:
            f1.write(datetime.datetime.now().strftime("%Y%m%d-%H%M")    + str(tweet.text.encode('utf8'))+'\n')
            analysis = TextBlob(tweet.text)
            tweet_polarity.append(analysis.sentiment.polarity)
        f1.flush()
        return tweet_polarity


parser = argparse.ArgumentParser(__file__, description="Stream sentiment")

parser.add_argument("--dataPath", "-p", dest='dataPath', help="Input a dataPath" )
args = parser.parse_args()
defaultPath="./data"
mypath=args.dataPath
if (mypath is None):
    mypath=defaultPath
mypath=mypath+"/"

sentiment = TweeterSentimentAnalyzer(mypath)

while (True):
    try:
        for ccy in sentiment.currencyLst:
            sentiment.readSentimentByTextBlob(ccy)
            logging.info(ccy+" sentiment ok")
        time.sleep(60)
    except:
        logging.error("Error connecting to tweeter")
        time.sleep(60)
    #quote.extractCrypto("ethereum")
    #quote.extractCrypto("iota")