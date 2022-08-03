import requests
import datetime
from datetime import timedelta
#from time import sleep
import pandas as pd
from fuzzywuzzy import fuzz
pd.set_option('display.max_columns', None)


class playerDataset:
    def __init__(self, date) -> None:
        self.date = date
        self.player_df = self.produce_df()

    
    def get_fpl_df(self):

        team_mapping = {
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

        base_url = 'https://fantasy.premierleague.com/api/'
        # get data from bootstrap-static endpoint
        r = requests.get(base_url+'bootstrap-static/').json()
        # get player data from 'elements' field
        players = r['elements']
        # create players dataframe
        players = pd.json_normalize(r['elements'])
        # get relevant columns
        players = players[['id', 'web_name', 'first_name', 'second_name', 'team', 'element_type']]
        players['full_name'] = players[['first_name', 'second_name']].apply(lambda x: ' '.join(x), axis=1)
        # map team number to team name
        players['team_name'] = players['team'].apply(lambda x: team_mapping[x])

        return players

    # Get the data from API

    def scrape_whoscored(self, id, homeTeam, awayTeam):
        url = f"https://api.sofascore.com/api/v1/event/{id}/lineups"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
        r = requests.get(url, headers=headers)
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
            #print(when)
            url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{when}"
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
            r = requests.get(url, headers=headers)
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

    def produce_df(self):
        fpl_df = self.get_fpl_df()
        print("got fpl players")
        all_players_df = self.goThroughGameDay(self.date, 6)
        print("got players from this gameweek")
        if (len(all_players_df) > 0):
            all_players_df['known_as'] = all_players_df.apply(lambda x: self.in_name2(x['player'], x['team_name'], fpl_df), axis=1)
            print("joined on similar names")
            return all_players_df
        else:
            return "Oops! Looks like the Premier League is on International Break."


