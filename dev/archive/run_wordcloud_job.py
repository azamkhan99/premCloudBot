import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import tweepy as tw
from wordcloud import STOPWORDS, WordCloud
import numpy as np
from PIL import Image
# import src.word_colouring as wc
import warnings
warnings.filterwarnings("ignore")

# sns.set(font_scale=1.5)
# sns.set_style("whitegrid")

class new_wordcloud:

    def __init__(self, player_df) -> None:
        
        self.players = player_df
        
        self.colour_teams = {
                '#EF0107': list(self.players['web_name'][self.players['team'] ==1]),
                '#95BFE5': list(self.players['web_name'][self.players['team'] ==2]),
                '#B50E12': list(self.players['web_name'][self.players['team'] ==3]),
                '#e30613': list(self.players['web_name'][self.players['team'] ==4]),
                '#0057B8': list(self.players['web_name'][self.players['team'] ==5]),
                '#6C1D45': list(self.players['web_name'][self.players['team'] ==6]),
                '#034694': list(self.players['web_name'][self.players['team'] ==7]),
                '#1B458F': list(self.players['web_name'][self.players['team'] ==8]),
                '#003399': list(self.players['web_name'][self.players['team'] ==9]),
                '#0d00e9': list(self.players['web_name'][self.players['team'] ==10]),
                '#dd0000': list(self.players['web_name'][self.players['team'] ==11]),
                '#000000': list(self.players['web_name'][self.players['team'] ==12]),
                '#97c1e7': list(self.players['web_name'][self.players['team'] ==13]),
                '#DA291C': list(self.players['web_name'][self.players['team'] ==14]),
                '#241F20': list(self.players['web_name'][self.players['team'] ==15]),
                '#e53233': list(self.players['web_name'][self.players['team'] ==16]),
                '#EE2737': list(self.players['web_name'][self.players['team'] ==17]),
                '#132257': list(self.players['web_name'][self.players['team'] ==18]),
                '#7A263A': list(self.players['web_name'][self.players['team'] ==19]),
                '#FDB913': list(self.players['web_name'][self.players['team'] ==20])
        }

        self.wordcloud = self.create_wordcloud()

    def import_df(self):
        players = pd.read_csv('src/players2.csv')
        players = players[['team_name', 'player', 'known_as']]
        players.fillna('', inplace=True)
        return players

    def additional_stopwords(self) -> None:
        self.stopwords_list.append('black')

        
    def get_tweet_count(self, player, bearer_token):
        client = tw.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
        query = player
        counts = client.get_recent_tweets_count(query=f"\"{query}\"", granularity='day')
        sum_tweets = 0
        for count in counts.data:
            sum_tweets += count['tweet_count']
        return sum_tweets


    def run_tweet_count(self, row, bearer_token):

        # if (row['known_as'] != '' and row['known_as'].lower() not in self.stopwords_list):
        #     return self.get_tweet_count(row['known_as'], bearer_token)
        # else:
        return self.get_tweet_count(row['player'], bearer_token)

    def run_twitter_queries(self, players): # Full name always method

        if (len(players) > 300):

            samples0 = players[0:300]
            samples1 = players[300:]
            samples0['number of tweets'] = samples0[['player','known_as']].apply(lambda x: self.get_tweet_count(x['player'], self.bearer_token1), axis=1)
            samples1['number of tweets'] = samples1[['player','known_as']].apply(lambda x: self.get_tweet_count(x['player'], self.bearer_token2), axis=1)
            samples = pd.concat([samples0, samples1])

            return samples
        else:
            samples = players
            samples['number of tweets'] = samples[['player','known_as']].apply(lambda x: self.get_tweet_count(x['player'], self.bearer_token1), axis=1)
            return samples


    def run_twitter_queries2(self, players): # New method (web name)

        if (len(players) > 300):

            samples0 = players[0:300]
            samples1 = players[300:]
            samples0['number of tweets'] = samples0[['player']].apply(lambda x: self.run_tweet_count(x, self.bearer_token1), axis=1)
            samples1['number of tweets'] = samples1[['player']].apply(lambda x: self.run_tweet_count(x, self.bearer_token2), axis=1)
            samples = pd.concat([samples0, samples1])

            return samples
        else:
            samples = players
            samples['number of tweets'] = samples[['player']].apply(lambda x: self.run_tweet_count(x, self.bearer_token1), axis=1)
            return samples



    def plot_cloud(wordcloud) -> None:
        # Set figure size
        plt.figure(figsize=(40, 20))
        # Display image
        plt.imshow(wordcloud) 
        # No axis details
        plt.axis("off")
        plt.tight_layout(pad=0);

    def create_wordcloud(self):

        samples = self.run_twitter_queries2(self.players)            
        players_dict = dict(samples[['player', 'number of tweets']].values)

        mask = np.array(Image.open('old_prem.png'))
        # # Generate wordcloud
        wordcloud = WordCloud(font_path='Staatliches-Regular.ttf', random_state=1, mask=mask, background_color="black", mode="RGBA", width=mask.shape[1],
                    height=mask.shape[0], colormap='Set2', collocations=False)
        wordcloud.generate_from_frequencies(players_dict)

        default_colour = 'grey'
        # grouped_colour_func = wc.SimpleGroupedColorFunc(self.colour_teams, default_colour)

        # wordcloud.recolor(color_func=grouped_colour_func)

        #wordcloud.to_file("wordcloudx.png")

        return wordcloud
    
        



