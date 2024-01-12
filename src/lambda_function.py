import os
from pathlib import Path
import tweepy
from run_get_data_job import playerDataset
from run_wordcloud_job import new_wordcloud
import datetime
import re

ROOT = Path(__file__).resolve().parents[0]


def get_tweet():
    """Get tweet to post"""

    #get players who played this week
    #get GW transferred_in count for each player
    #create wordcloud
    
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    #date = '2022-05-22'
    
    player_df = playerDataset(date).player_df
    if (type(player_df) == str):
        text = 'Oops! Looks like the Premier League is on International Break :\'('
        return player_df, text
    else:
        print("initi wordcloud")
        wordcloud = new_wordcloud(player_df).wordcloud
        text = "🔄 FPL Transfer Buzz! Check out this Word Cloud highlighting this week's most transferred-in Premier League players. ⚽📊 #FPL #GameweekTrends"
        return wordcloud, text


   


def lambda_handler(event, context):
    print("Get credentials")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    tweepy_auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    tweepy_api = tweepy.API(tweepy_auth)

    client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

    print("Get tweet")
    media, tweet = get_tweet()

    media.to_file("/tmp/media.png")

    print(f"Post tweet: {tweet}")
    post = tweepy_api.simple_upload("/tmp/media.png")
    text = str(post)
    media_id = re.search("media_id=(.+?),", text).group(1)
    
    client.create_tweet(text=tweet, media_ids = [media_id],user_auth=True)

    return {"statusCode": 200, "tweet": tweet}
