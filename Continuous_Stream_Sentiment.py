# import tweepy library for twitter api access and textblob libary for sentiment analysis
import csv
import tweepy
import numpy as np
from textblob import TextBlob
import datetime
import time

def main():

    # set twitter api credentials
    consumer_key= 'JbZWz1hekxkCv1sCRW6k9BrjF'
    consumer_secret= 'tjZclsG6BqdGNfnUAt1wAFRzBX3PXHDGp6z54jKryVHJN3wWOo'
    access_token='926643380-mTGIw7bfYqF6sxbiZqNZb0LCdBypqAtIEC4rPtll'
    access_token_secret='4hetDuuv5lDtzzAPzyN1E1a5XX41bJeQNATggb0Mwqf3m'

    # set path of csv file to save sentiment stats
    path = 'live_tweet2.csv'
    f = open(path,"a")
    f1 = open('tweet_data','a')
    # access twitter api via tweepy methods
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter_api = tweepy.API(auth)

    while True:

        # fetch tweets by keywords
        tweets = twitter_api.search(q=['bitcoin, price, crypto'], count=100)

        # get polarity
        polarity = get_polarity(tweets,f1)
        sentiment = np.mean(polarity)

        # save sentiment data to csv file
        f.write(str(sentiment))
        f.write(","+datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
        f.write("\n")
        f.flush()
        time.sleep(60)
    

def get_polarity(tweets,f):
    # run polarity analysis on tweets

    tweet_polarity = []

    for tweet in tweets:
        f.write(str(tweet.text.encode('utf8'))+'\n')
        analysis = TextBlob(tweet.text)
        tweet_polarity.append(analysis.sentiment.polarity)

    return tweet_polarity

main()
