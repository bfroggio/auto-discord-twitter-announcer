import secrets
import tweepy
import time
import requests
import re
from discord import Webhook, RequestsWebhookAdapter

username='BFroggio'
user_id="1287382415225303040" #BFroggio

api = tweepy.Client(secrets.bearer_token, secrets.consumer_key, secrets.consumer_secret, secrets.access_token, secrets.access_token_secret)

last_announced_tweet=0

while True:
    tweets_list= api.get_users_tweets(id=user_id) # Get the latest tweets
    tweet= tweets_list[0][0] # Grab the most recent tweet

    #  print(tweet)

    if tweet.id != last_announced_tweet:
        contains_twitch_link=False
        all_urls_in_tweet= re.findall(r'(https?://[^\s]+)', tweet.text)

        for url in all_urls_in_tweet:
            resp = requests.head(url)

            #  print(resp.headers["Location"])

            if "Location" in resp.headers and "twitch.tv/bfroggio" in resp.headers["Location"]:
                contains_twitch_link= True

        if contains_twitch_link or "#announcement" in tweet.text:
            last_announced_tweet= tweet.id
            #  print(tweet.id)
            tweet_link="https://twitter.com/"+username+"/status/"+str(tweet.id)
            webhook = Webhook.from_url(secrets.discord_webhook, adapter=RequestsWebhookAdapter())
            webhook.send(tweet_link)
            #  print(tweet_link)

    time.sleep(5)
