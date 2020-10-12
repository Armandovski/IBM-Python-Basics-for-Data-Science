"""
Created on Sat Oct 10 15:39:53 2020

@author: Armando Alvarez Rolins

This code is a practice on how to use the NBA Stats API. Documentation can be
found on the links below:
    
    https://github.com/swar/nba_api/blob/master/docs/table_of_contents.md
    
    https://pypi.org/project/nba-api/
"""
import pandas as pd
import matplotlib.pyplot as plt

#!pip install nba_api

#This function takes in data in list format and transforms it into dictionary
def one_dict(list_dict):
    keys=list_dict[0].keys()
    out_dict={key:[] for key in keys}
    for dict_ in list_dict:
        for key, value in dict_.items():
            out_dict[key].append(value)
    return out_dict

#For Static usage, import static library (players or teams)
from nba_api.stats.static import teams

#Get all teams
nba_teams = teams.get_teams()

#Convert nba_teams from list to dictionary then make it into Panda dataframe
dict_nba_teams = one_dict(nba_teams)
df_teams = pd.DataFrame(dict_nba_teams)

#Will use a team's nickname to find the unique id
df_warriors = df_teams[df_teams['nickname']=='Warriors']
id_warriors = df_warriors[['id']].values[0][0]

#Import endpoint "/leaguegamefinder"
from nba_api.stats.endpoints import leaguegamefinder

#The function "League Game Finder" will make an API call
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=id_warriors)
games = gamefinder.get_data_frames()[0]

#Create two data frames: for games vs. TOR Raptors at home and away
games_home = games [games ['MATCHUP']=='GSW vs. TOR']
games_away = games [games ['MATCHUP']=='GSW @ TOR']

#Plot tje PLUS MINUS column and see if they played better at home or away
fig, ax = plt.subplots()

games_away.plot(x='GAME_DATE',y='PLUS_MINUS', ax=ax)
games_home.plot(x='GAME_DATE',y='PLUS_MINUS', ax=ax)
ax.set_ylabel('Point Difference')
ax.set_xlabel('Game Date')
ax.legend(["Away", "Home"])
plt.show()