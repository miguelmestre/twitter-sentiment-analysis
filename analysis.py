
from typing import Text
from tweepy import API,  OAuthHandler
from textblob import TextBlob
import os
from dotenv import load_dotenv


class TwitterAnalysis():

    def __init__(self):
        load_dotenv()
        api_key=os.environ.get("API-KEY", None)
        api_secret_key=os.environ.get("API-SECRET", None)
        authentication = OAuthHandler(api_key, api_secret_key)
        self.api = API(authentication)

    def main(self):
        topic, number = self.ask()
        tweets = self.api.search(topic, lang="en", count=number)
        normalized_tweets = [self.normalize_tweets(tweet.text) for tweet in tweets]
        return self.analyze_tweets(normalized_tweets)

    def ask(self):
        """Asks user which topic and the number of tweets to analyze"""
        topic = input("Which topic you want to perform analysis?")
        while True:
            number = input("How many tweets you want to analyze (max:100) ?")
            if not number.isdigit() or int(number) > 100 or int(number) < 1:
                print("Invalid")
                continue
            else:
                return topic, number

    def normalize_tweets(self, tweet):
        """ Normalizes the tweet """
        tweet_words = tweet.split(' ')
        normalized_tweet = [word for word in tweet_words if not word.startswith('#')]
        return ' '.join(normalized_tweet)
        
    def analyze_tweets(self, tweets):
        """ Function that analyzes the tweets"""
        negative_tweets = list()
        positive_tweets = list()
        for tweet in tweets:
            tweet_polarity = TextBlob(tweet).sentiment.polarity
            if tweet_polarity<0:
                negative_tweets.append(tweet)
                continue
            positive_tweets.append(tweet)
        return positive_tweets, negative_tweets

positive, negative = TwitterAnalysis().main()
print("Positive tweets:")
print(positive)
print("Negative tweets:")
print(negative)
print(len(positive), ' VS  ', len(negative))
