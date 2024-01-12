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
        
        self.bearer_token = 'AAAAAAAAAAAAAAAAAAAAADSvdgEAAAAA8cjhwVlgHxfqrl8B3tAPo8N3ZDY%3DbsIf3O2IuSVcSKgWU2LRZxwqu2W8ULEonebjvvyhshpKPDZqsD'
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

        self.wordcloud = self.create_wordcloud(self.players, 'transfers_in_event')


    def _df_to_dict(self,df, value):
        player_dic = {}
        for web_name, first_name, second_name, value in df[['web_name', 'first_name', 'second_name', value]].values:
            key = first_name + ' ' + second_name if web_name in player_dic else web_name
            player_dic[key] = value

        return player_dic

    def plot_cloud(wordcloud) -> None:
        # Set figure size
        plt.figure(figsize=(40, 20))
        # Display image
        plt.imshow(wordcloud) 
        # No axis details
        plt.axis("off")
        plt.tight_layout(pad=0);

    def create_wordcloud(self,players_df, ranking_value):

        players_dict = self._df_to_dict(players_df, ranking_value)

        mask = np.array(Image.open('old_prem.png'))
        # # Generate wordcloud
        wordcloud = WordCloud(font_path='Staatliches-Regular.ttf', random_state=1, mask=mask, background_color="grey", mode="RGBA", width=mask.shape[1],
                    height=mask.shape[0], colormap='Set2', collocations=False, max_words=1000)
        wordcloud.generate_from_frequencies(players_dict)

        default_colour = 'white'
        grouped_colour_func = wc.SimpleGroupedColorFunc(self.colour_teams, default_colour)

        wordcloud.recolor(color_func=grouped_colour_func)

    #     wordcloud.to_file("wordcloudx.png")

        return wordcloud
    
        



