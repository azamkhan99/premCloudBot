import os
from pathlib import Path
import tweepy
import run_get_data_job
import run_wordcloud_job
import datetime

ROOT = Path(__file__).resolve().parents[0]


def get_tweet():
    """Get tweet to post"""

    #get players who played this week
    #get count of tweets for each player
    #create wordcloud
    
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    #date = '2022-05-22'
    
    player_df = run_get_data_job.playerDataset(date).player_df
    if (type(player_df) == str):
        text = 'Oops! Looks like the Premier League is on International Break :\'('
        return player_df, text
    else:
        print("initi wordcloud")
        wordcloud = run_wordcloud_job.new_wordcloud(player_df).wordcloud
        text = "#FPL #PL\nA Word cloud of Premier League players who participated in the most recent Matchweek!"
        return wordcloud, text


   


def lambda_handler(event, context):
    print("Get credentials")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print("Get tweet")
    media, tweet = get_tweet()

    media.to_file("/tmp/media.png")

    print(f"Post tweet: {tweet}")
    api.update_status_with_media(status=tweet, filename='/tmp/media.png')

    return {"statusCode": 200, "tweet": tweet}
