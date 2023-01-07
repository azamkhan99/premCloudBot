import requests
import datetime
from datetime import timedelta
#from time import sleep
import pandas as pd
from fuzzywuzzy import fuzz
from fplapi import main
import asyncio
import boto3
pd.set_option('display.max_columns', None)


class playerDataset:
    def __init__(self, date) -> None:
        self.date = date
        self.player_df = self.produce_df()

    
    def get_fpl_df(self):
        key = 'fpl_players.csv'
        bucket = 'premcloudbot'
        s3_client = boto3.client('s3')
        
        
        # for key in s3_resource.list_objects(Bucket=bucket)['Contents']:
        #     print(key['Key'])
        
        resp = s3_client.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(resp['Body'], sep=',')
        #df = pd.read_csv(data)
        # df = pd.read_csv('fpl_players.csv')
        print(df.sample(2))

        return df

    # Get the data from API

    def scrape_whoscored(self, id, homeTeam, awayTeam):
        url = f"https://api.sofascore.com/api/v1/event/{id}/lineups"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}

        r = requests.get(url, headers=headers, proxies = {'http': '133.18.195.135:8080'})
        json_data = r.json()
        home_players_json = json_data["home"]["players"]
        away_players_json = json_data["away"]["players"]

        ls = []

        for player in home_players_json:
            ls.append((player["player"]["name"], homeTeam))

        for player in away_players_json:
            ls.append((player["player"]["name"], awayTeam))
            
        return ls

    
    

    def goThroughGameDay(self, start_date, days):

        def flatten(xss):
            return [x for xs in xss for x in xs]

        def Convert(tup, di):
            for b, a in tup:
                di.setdefault(a, []).append(b)
            return di
        
        ids = {}
        for day in range(days):
            when = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() - timedelta(days=day)
            url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{when}"
            r = requests.get(url, headers={'User-Agent': 'Firefox/66.0'}, proxies = {'http': '133.18.195.135:8080'})
            json_data = r.json()

            for x in json_data['events']:
                if(x['tournament']['name'] == 'Premier League' and x['tournament']['category']['name'] == 'England') \
                    and x['id'] not in ids:
                    ids[x['id']] = (x['homeTeam']['name'], x['awayTeam']['name'])

            del json_data

        allPlayers = []
        for i in ids.keys():
            allPlayers.append(self.scrape_whoscored( i, ids[i][0], ids[i][1] ))
            #add wait sleep(5)
        
        tup = list(set(flatten(allPlayers)))
        dc = {}

        di = Convert(tup, dc)

        return (pd.DataFrame([(key, var) for (key, L) in di.items() for var in L], 
                    columns=['team_name', 'player']))


    def in_name2(self, player, team_name, fpl_df):
        ls = []
        for x in range(len(fpl_df['full_name'][fpl_df['team_name'] == team_name])):
            if (fuzz.token_set_ratio(fpl_df['full_name'][fpl_df['team_name'] == team_name].iloc[x], player)) >= 88:
                ls.append(fpl_df['web_name'][fpl_df['team_name'] == team_name].iloc[x])
        if (len(ls)>0):
            return ls[0]
        else:
            return ''
#:)
    def produce_df(self):
        fpl_df = self.get_fpl_df()
        print("got fpl players")
        # return fpl_df
        all_players_df = self.goThroughGameDay(self.date, 3)
        print("got players from this gameweek")
        if (len(all_players_df) > 0):
            all_players_df['known_as'] = all_players_df.apply(lambda x: self.in_name2(x['player'], x['team_name'], fpl_df), axis=1)
            print("joined on similar names")
            return all_players_df
        else:
            return "Oops! Looks like the Premier League is on International Break."


