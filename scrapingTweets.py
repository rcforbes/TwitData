import tweepy
import json
import csv
import re
import pandas as pd
import uuid

def search_for_tweets(consumer_key, consumer_secret, access_token, access_token_secret, n_tweets):
    
    #authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy
    api = tweepy.API(auth)
    
    rows = []
    #for each tweet that includes "inaugeration", write relevant info to the spreadsheet
    for tweet in tweepy.Cursor(api.search, q="inaugeration-filter:retweets", 
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
#hashtag_phrase = input('Hashtag Phrase: ') # include '#' when searching for hashtag - this script can be used to search for any phrase or hashtag
n_tweets = int(input('Number of Tweets: '))


rows_df = search_for_tweets(consumer_key=consumer_key, 
                              consumer_secret=consumer_secret, 
                              access_token_secret=access_token_secret, 
                              access_token=access_token,
                              n_tweets=n_tweets)


rows_df.columns = ['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count', 'retweet_count', 'likes_count', 'uniqueID']

rows_df.head()

rows_df.to_csv('tweets.csv') 


    
