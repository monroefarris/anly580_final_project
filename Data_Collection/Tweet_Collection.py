#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import tweepy   # Note: Tweepy should be v3.10.0
from tweepy import OAuthHandler
import pandas as pd
import re
from datetime import datetime
import yaml


# Get information about a certain tweet 
def get_tweet_data(tweet, column_names):
    
    # Get the user screen name
    user_screen_name = tweet.user.screen_name

    ###############
    ### Get user mention data for tweet
    ###############
    
    # Instantiate empty lists to hold user mention data: id's & screen names
    user_mention_ids = []
    user_mention_screen_names = []

    # Get the user_mentions entity of the status
    user_mentions = tweet.entities['user_mentions']
    
    # Loop through the user mention data and append id & screen names to lists
    for user in user_mentions:
        user_mention_ids.append(user['id'])
        user_mention_screen_names.append(user['screen_name'])

    ###############
    ### Get hashtag data for tweet
    ###############
    
    # Instantiate empty list to hold hashtag data
    hashtags = []

    # Get the hashtag entity of the status
    hashtag_entity = tweet.entities['hashtags']
    
    # Loop through the hashtag data and append text to list
    for ht in hashtag_entity:
        hashtags.append(ht['text'])

    ###############
    ### Clean tweets: remove urls, hashtags, mentions, and non-English characters 
    ### Reference: https://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
    ### Reference: https://stackoverflow.com/questions/42370508/how-to-delete-special-characters-such-as-ŒðŸ-from-tweets
    ###############
    
    # Get the text of the tweet
    text = tweet.full_text
    
    # Remove urls from tweets
    text_re = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)',
                         re.DOTALL)
    text_re2 = re.findall(text_re, text)
    for t in text_re2:
        text = text.replace(t[0], ', ') 
    
    # Remove hashtags & mentions from tweets
    prefixes = ['@','#']
    all_words = text.split()
    words_to_keep = []
    if len(all_words) >= 1:
        for word in all_words:
            if word[0] not in prefixes:
                words_to_keep.append(word)
    text = ' '.join(words_to_keep)
    
    # Remove non-English from tweets
    text = ''.join([char for char in text if ord(char) < 128])
        
    ###############
    ### Add all tweet attributes into dataframe
    ###############
    
    # Make list of tweet attributes to add to data frame
    list_tweets = [
                   # The time the status was posted.
                   tweet.created_at, #str(tweet.created_at.date()),
                   # The text of the status.
                   text, 
                   # The hashtags of the status
                   hashtags,
                   # The id's of the user_mentions of the status
                   user_mention_ids,
                   # The screen names of the user_mentions of the status
                   user_mention_screen_names,                      
                   # The number of retweets of the status.
                   tweet.retweet_count,
                   # The number of likes of the status.
                   tweet.favorite_count,
                   # The ID of the user being replied to.
                   tweet.in_reply_to_user_id,
                   # The screen name of the user being replied to
                   tweet.in_reply_to_screen_name,
                   # The geo object of the status.
                   tweet.geo,
                   # The coordinates of the status.
                   tweet.coordinates,

                   # user : The User object of the poster of the status.
                   tweet.user.id,
                   user_screen_name,
                   tweet.user.name,
                   tweet.user.location,
                   tweet.user.friends_count,
                   tweet.user.followers_count,
                   tweet.user.favourites_count,
                   tweet.user.verified,
                   tweet.user.statuses_count
                   ]
    
    # Return the tweet data
    return list_tweets


### Method for collecting tweets
def get_tweets(search_words, date_start, date_end, num_tweets, column_names):
    
    # Create dataframe to hold the twitter data, with specified headers
    tweet_data = pd.DataFrame(columns=column_names)
    
    # Get all tweets with specified search word
    tweets_all = tweepy.Cursor(api.search, 
                               q=search_words + " -filter:retweets",
                               lang="en",
                               since = date_start,
                               until = date_end,
                               tweet_mode='extended').items(num_tweets)

    # Loop through tweets
    for tweet in tweets_all:
        
        # Get information about each tweet
        tweet_info = get_tweet_data(tweet, column_names)

        # Append tweet's information to dataframe
        tweet_data.loc[len(tweet_data)] = tweet_info
    
    # Return the tweet data
    return tweet_data


if __name__ == "__main__":

    ### Read in yml file
    with open('collection_data.yml', 'r') as file:
        inputs = yaml.safe_load(file)
    
    ### Set up Twitter API info & Tweepy
    auth = OAuthHandler(inputs['consumer_key'], inputs['consumer_secret'])
    auth.set_access_token(inputs['access_token'], inputs['access_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    ### Specify details for tweet collection
        
    # Specify dataframe column names
    column_names = [
                    # Data about tweet
                    'created_at', 
                    'text',
                    'hashtags',
                    'user_mention_ids',
                    'user_mention_screen_names',
                    'retweet_count',
                    'favorite_count',
                    'in_reply_to_user_id',
                    'in_reply_to_screen_name',
                    'geo',
                    'coordinates',

                    # Data about tweet creater
                    'user_id',
                    'user_screen_name',
                    'user_name',
                    'user_location',
                    'user_friends_count', 
                    'user_followers_count',
                    'user_favourites_count',
                    'user_verfied',
                    'user_statuses_count'
                    ]

    # Specify start and end date of gathering tweets
    start_date =  datetime.strptime(inputs['start_date'], '%m/%d/%y %H:%M:%S')
    end_date =  datetime.strptime(inputs['end_date'], '%m/%d/%y %H:%M:%S')

    # Specify number of tweets to collect
    num_tweets = inputs['num_tweets']

    # Indicate keyword to search
    search_words = inputs['search_words']

    # Get tweets about keyword of interest
    tweet_data = get_tweets(search_words = search_words, 
                            date_start = start_date,
                            date_end = end_date,
                            num_tweets = num_tweets,
                            column_names = column_names)

    # Export tweet data to csv file
    if inputs['save_to_csv']:
        tweet_data.to_csv(inputs['tweet_filename'], index = False)
