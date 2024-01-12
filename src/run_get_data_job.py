import requests
import datetime
from datetime import timedelta
#from time import sleep
import pandas as pd
from fuzzywuzzy import fuzz
#from fplapi import main
import asyncio
import boto3
import urllib3
import json
pd.set_option('display.max_columns', None)


class playerDataset:
    def __init__(self, date) -> None:
        self.date = date
        self.player_df = self.get_fpl_df()

    def get_team(df,team_name):
        res = df[df['name'] == team_name]
        if len(res) == 0:
            return None
        else:
            return res

    
    def get_fpl_df(self):
            """
            Retrieves player data from the Fantasy Premier League API and returns a dataframe.

            Returns:
                players (pandas.DataFrame): Dataframe containing player information.
            """
            base_url = 'https://fantasy.premierleague.com/api/'
            # get data from bootstrap-static endpoint
            http = urllib3.PoolManager()

            r = http.request('GET', base_url+'bootstrap-static/', headers = {        
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',        
                    'Accept-Encoding': 'gzip, deflate, br',        
                    'Accept-Language': 'en-US,en;q=0.5',        
                    'Connection': 'keep-alive',        
                    'Cookie': 'AMCV_0D15148954E6C5100A4C98BC%40AdobeOrg=1176715910%7CMCIDTS%7C19271%7CMCMID%7C80534695734291136713728777212980602826%7CMCAAMLH-1665548058%7C7%7CMCAAMB-1665548058%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1664950458s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19272%7CvVersion%7C5.4.0; s_ecid=MCMID%7C80534695734291136713728777212980602826; __cfruid=37ff2049fc4dcffaab8d008026b166001c67dd49-1664418998; AMCVS_0D15148954E6C5100A4C98BC%40AdobeOrg=1; s_cc=true; __cf_bm=NIDFoL5PTkinis50ohQiCs4q7U4SZJ8oTaTW4kHT0SE-1664943258-0-AVwtneMLLP997IAVfltTqK949EmY349o8RJT7pYSp/oF9lChUSNLohrDRIHsiEB5TwTZ9QL7e9nAH+2vmXzhTtE=; PHPSESSID=ddf49facfda7bcb4656eea122199ea0d',                        
                    'If-Modified-Since': 'Tue, 04 May 2021 05:09:49 GMT',        
                    'If-None-Match': 'W/"12c6a-5c17a16600f6c-gzip"',        
                    'Sec-Fetch-Dest': 'document',        
                    'Sec-Fetch-Mode': 'navigate',        
                    'Sec-Fetch-Site': 'none',        
                    'Sec-Fetch-User': '?1',        
                    'TE': 'trailers',        
                    'Upgrade-Insecure-Requests': '1',        
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'        
                })
            print(r.status)
            dic = json.loads(r.data.decode('utf-8'))
            # get player data from 'elements' field
            players = pd.json_normalize(dic['elements'])
            # create players dataframe
            # get relevant columns
            players = players[['id', 'web_name', 'first_name', 'second_name', 'team', 'transfers_in', 'transfers_out', 'transfers_in_event', 'transfers_out_event', 'selected_by_percent', 'element_type']]
            print(players.iloc[0])

            return players

    

    # def did_player_play(self, player_id):
    #     r = requests.request(method = "GET",url=f"https://fantasy.premierleague.com/api/element-summary/{player_id}/")
    #     r = r.json()
    #     if len(r['history']) == 0:
    #         return False
    #     minutes = r['history'][-1]['minutes']
    #     if minutes > 0:
    #         return True
    #     else:
    #         return False
        
    # def goThroughGameDay(self, gw, fpl_df):
    #     url = f'https://fantasy.premierleague.com/api/event/{gw}/live/'
    #     r = requests.request(method = "GET",url=url)
    #     r = r.json()
    #     r = pd.json_normalize(r['elements'])
    #     r = r[r['stats.minutes'] > 0]
    #     r = r['id']

    #     filtered_dataset = pd.merge(fpl_df, r, how='inner', left_on='id', right_on='id')
    #     filtered_dataset = filtered_dataset[['team_name', 'web_name']]
    #     filtered_dataset.rename(columns={'web_name': 'player'}, inplace=True)
    #     return filtered_dataset



    # def in_name2(self, player, team_name, fpl_df):
    #     ls = []
    #     for x in range(len(fpl_df['full_name'][fpl_df['team_name'] == team_name])):
    #         if (fuzz.token_set_ratio(fpl_df['full_name'][fpl_df['team_name'] == team_name].iloc[x], player)) >= 88:
    #             ls.append(fpl_df['web_name'][fpl_df['team_name'] == team_name].iloc[x])
    #     if (len(ls)>0):
    #         return ls[0]
    #     else:
    #         return ''
#:)
    # def produce_df(self):
    #     fpl_df = self.get_fpl_df()
    #     print("got fpl players")
    #     # return fpl_df
    #     all_players_df = self.goThroughGameDay(2, fpl_df)
    #     print("got players from this gameweek")
    #     if (len(all_players_df) > 0):
    #         # all_players_df['known_as'] = all_players_df.apply(lambda x: self.in_name2(x['player'], x['team_name'], fpl_df), axis=1)
    #         # print("joined on similar names")
    #         return all_players_df
    #     else:
    #         return "Oops! Looks like the Premier League is on International Break."


