import tweepy
import json
import csv
import re
import pandas as pd
import uuid

#/Users/rachelforbes/opt/anaconda3/bin/python3 /Users/rachelforbes/Desktop/TwitData/scrapingTwitter.py

def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase, n_tweets):
    
    #authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy
    api = tweepy.API(auth)
    
    rows = []
    #for each tweet matching our hashtags, write relevant info to the spreadsheet
    for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets', 
                                   lang="en", tweet_mode='extended').items(n_tweets):
    #print(str(tweet))
        row = [tweet.created_at, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'),
         [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count, tweet.retweet_count, tweet.favorite_count, uuid.uuid4()]
        rows.append(row)
    return pd.DataFrame(rows)

consumer_key = input('Consumer Key: ')
consumer_secret = input('Consumer Secret: ')
access_token = input('Access Token: ')
access_token_secret = input('Access Token Secret: ')
hashtag_phrase = input('Hashtag Phrase: ') # include '#' when searching for hashtag
n_tweets = int(input('Number of Tweets: '))


rows_df = search_for_hashtags(consumer_key=consumer_key, 
                              consumer_secret=consumer_secret, 
                              access_token_secret=access_token_secret, 
                              access_token=access_token, 
                              hashtag_phrase=hashtag_phrase, 
                              n_tweets=n_tweets)


rows_df.columns = ['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count', 'retweet_count', 'likes_count', 'uniqueID']

rows_df.head()

rows_df.to_csv('tweets.csv') #not saving to wd bc python issue


"""
from pyspark import SparkContext 
from pyspark.sql import SQLContext 
from pyspark.sql import functions as F
import pandas as pd 
sc=SparkContext()
sqlc=SQLContext(sc) 
df=pd.read_csv(<YOUR PATH HERE>) 
sdf=sqlc.createDataFrame(df) 

"""

    