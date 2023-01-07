import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import tweepy as tw
from wordcloud import STOPWORDS, WordCloud
import numpy as np
from PIL import Image
import word_colouring as wc
import warnings
warnings.filterwarnings("ignore")

# sns.set(font_scale=1.5)
# sns.set_style("whitegrid")

class new_wordcloud:

    def __init__(self, player_df) -> None:
        
        self.bearer_token1 = 'AAAAAAAAAAAAAAAAAAAAADSvdgEAAAAAmw3P5GYdOs4kanpVkdzMKp0zOck%3DgmSSBWJtumsCQ2aaycMaMcvlQ4vIeVEtCXnCjvsYrGPKFZAy4g'
        self.bearer_token2 = 'AAAAAAAAAAAAAAAAAAAAAHjCfAEAAAAAu29%2BwwrHh6tEGPqCJ8VNeN77XgQ%3Dlq53xeUMIFpHb35KyRlYno7DQr2bZ0q2fgXEGf5GTp9v5VLInJ'
        #self.players = self.import_df()
        self.players = player_df
        self.team_mapping = {

            1: "Arsenal",
            2: "Aston Villa",
            3: "AFC Bournemouth",
            4: "Brentford",
            5: "Brighton & Hove Albion",
            6: "Chelsea",
            7: "Crystal Palace",
            8: "Everton",
            9: "Fulham",
            11: "Leeds United",
            10: "Leicester City",
            12: "Liverpool",
            13: "Manchester City",
            14: "Manchester United",
            15: "Newcastle United",
            16: "Nottingham Forest",
            17: "Southampton",
            18: "Tottenham Hotspur",
            19: "West Ham United",
            20: "Wolverhampton"
        }
        self.colour_teams = {
            '#c70000': list(self.players['player'][self.players['team_name'] == "Arsenal"]),
            '#7b003a': list(self.players['player'][self.players['team_name'] == "Aston Villa"]),
            '#e30613': list(self.players['player'][self.players['team_name'] == "Brentford"]),
            '#005daa': list(self.players['player'][self.players['team_name'] == "Brighton & Hove Albion"]),
            '#800000': list(self.players['player'][self.players['team_name'] == "Burnley"]),
            '#0000dd': list(self.players['player'][self.players['team_name'] == "Chelsea"]),
            '#0a4af5': list(self.players['player'][self.players['team_name'] == "Crystal Palace"]),
            '#0d00e9': list(self.players['player'][self.players['team_name'] == "Everton"]),
            '#ffed00': list(self.players['player'][self.players['team_name'] == "Leeds United"]),
            '#0101e8': list(self.players['player'][self.players['team_name'] == "Leicester City"]),
            '#dd0000': list(self.players['player'][self.players['team_name'] == "Liverpool"]),
            '#97c1e7': list(self.players['player'][self.players['team_name'] == "Manchester City"]),
            '#e80909': list(self.players['player'][self.players['team_name'] == "Manchester United"]),
            '#000000': list(self.players['player'][self.players['team_name'] == "Newcastle United"]),
            '#ffee00': list(self.players['player'][self.players['team_name'] == "Norwich City"]),
            '#ff0000': list(self.players['player'][self.players['team_name'] == "Southampton"]),
            '#ffffff': list(self.players['player'][self.players['team_name'] == "Tottenham Hotspur"]),
            '#fbee23': list(self.players['player'][self.players['team_name'] == "Watford"]),
            '#7f0000': list(self.players['player'][self.players['team_name'] == "West Ham United"]),
            '#fdbc02': list(self.players['player'][self.players['team_name'] == "Wolverhampton"]),
            '#000040': list(self.players['player'][self.players['team_name'] == "Fulham"]),
            '#8b0304': list(self.players['player'][self.players['team_name'] == "AFC Bournemouth"]),
            '#e53233': list(self.players['player'][self.players['team_name'] == "Nottinham Forest"])
            }
        self.stopwords_list = list(STOPWORDS)
        self.additional_stopwords()

        self.wordcloud = self.create_wordcloud()

    def import_df(self):
        players = pd.read_csv('src/players2.csv')
        players = players[['team_name', 'player', 'known_as']]
        players.fillna('', inplace=True)
        return players

    def additional_stopwords(self) -> None:
        self.stopwords_list.append('black')
        self.stopwords_list.append('gray')
        self.stopwords_list.append('white')
        self.stopwords_list.append('green')
        self.stopwords_list.append('brown')
        self.stopwords_list.append('grey')
        self.stopwords_list.append('blue')
        self.stopwords_list.append('wood')
        self.stopwords_list.append('cash')
        self.stopwords_list.append('sá')
        self.stopwords_list.append('jones')
        self.stopwords_list.append('james')
        self.stopwords_list.append('thomas')
        self.stopwords_list.append('sánchez')
        self.stopwords_list.append('son')
        self.stopwords_list.append('holding')
        self.stopwords_list.append('dele')
        self.stopwords_list.append('johnson')
        self.stopwords_list.append('burn')
        self.stopwords_list.append('march')
        self.stopwords_list.append('rice')
        self.stopwords_list.append('henry')
        self.stopwords_list.append('palmer')
        self.stopwords_list.append('young')
        self.stopwords_list.append('evans')
        self.stopwords_list.append('pérez')
        self.stopwords_list.append('bueno')
        self.stopwords_list.append('dias')
        self.stopwords_list.append('pérez')
        self.stopwords_list.append('taylor')
        self.stopwords_list.append('cook')
        self.stopwords_list.append('justin')
        self.stopwords_list.append('hill')
        self.stopwords_list.append('anthony')
        self.stopwords_list.append('smith')
        
    def get_tweet_count(self, player, bearer_token):
        client = tw.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
        query = player
        counts = client.get_recent_tweets_count(query=f"\"{query}\"", granularity='day')
        sum_tweets = 0
        for count in counts.data:
            sum_tweets += count['tweet_count']
        return sum_tweets


    def run_tweet_count(self, row, bearer_token):

        if (row['known_as'] != '' and row['known_as'].lower() not in self.stopwords_list):
            return self.get_tweet_count(row['known_as'], bearer_token)
        else:
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
            samples0['number of tweets'] = samples0[['player','known_as']].apply(lambda x: self.run_tweet_count(x, self.bearer_token1), axis=1)
            samples1['number of tweets'] = samples1[['player','known_as']].apply(lambda x: self.run_tweet_count(x, self.bearer_token2), axis=1)
            samples = pd.concat([samples0, samples1])

            return samples
        else:
            samples = players
            samples['number of tweets'] = samples[['player','known_as']].apply(lambda x: self.run_tweet_count(x, self.bearer_token1), axis=1)
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
        grouped_colour_func = wc.SimpleGroupedColorFunc(self.colour_teams, default_colour)

        wordcloud.recolor(color_func=grouped_colour_func)

        #wordcloud.to_file("wordcloudx.png")

        return wordcloud
    
        



