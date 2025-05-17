import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import teams
from nba_api.stats.endpoints import CommonPlayerInfo
import datetime
import time


def retry_api_call(func, *args, max_retries=3, delay=3, **kwargs):
    attempts = 0
    while attempts < max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts} failed with error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2
    raise Exception(f"Failed after {max_retries} retries.")



#gets a list of dictionaries with every active player in nba
def getAllActivePlayers():
    nba_players = players.get_active_players()
    #print("Accessing all active NBA players")
    return nba_players
#gets a list of dictionaries with every team in the nba
def getAllTeams():
    nba_teams = teams.get_teams()
    return nba_teams



def get_player_team_id(player_id):
    info = CommonPlayerInfo(player_id=player_id)
    df = info.get_data_frames()[0]
    team_id = df.loc[0, 'TEAM_ID']
    print(team_id)
    return team_id



#takes the current date and calculates the current nba season and formats it correctly
def getCurrentRegularSeasonDate():

    regular_season_start = 0
    regular_season_end = 0
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    # nba regular season starts in october and ends in april
    if current_month >= 10:
        regular_season_start = current_year
        regular_season_end = current_year + 1
    else:
        regular_season_start = current_year - 1
        regular_season_end = current_year

    if regular_season_end % 100 > 9:
        regular_season_end_formatted = regular_season_end % 100
    else:
        zero_string = "0"
        regular_season_end_formatted = regular_season_end % 100
        str(regular_season_end_formatted)
        regular_season_end_formatted = zero_string + regular_season_end_formatted

    return f"{regular_season_start}-{regular_season_end_formatted}" #should return a year in form ex: 2014-15
#gets the player ID from looping through all active players
def get_ID(nba_players, first_name, last_name):
    for player in nba_players:
        player_full_name = f"{first_name} {last_name}"
        if player_full_name == player['full_name']:
            #print(f"{first_name} {last_name}'s player ID is {player['id']}")
            return player['id']
    return None
#gets team id from team name
def get_Team_ID_From_Full_Name(nba_teams, opposing_team):
    for team in nba_teams:
        if opposing_team == team['full_name']:
            #print(f"The opposing team the {opposing_team}'s team ID is {team['id']}")
            return team['id']
    return None
#gets team id from abbreviation
def get_Team_ID_From_Abbreviation(nba_teams, abbreviation):
    for team in nba_teams:
        if team['abbreviation'] == abbreviation:
            return team['id']
    return None

#if you dont know the team name but know the abbreviation
def get_Full_Name_From_Abbreviation(nba_teams, opponent_abbreviation):
    for team in nba_teams:
        if opponent_abbreviation == team['abbreviation']:
            #print(f"The opposing {opponent_abbreviation}'s team name is {team['full_name']}")
            return team['full_name']
    return None
#if you dont know the abbreviation but know the team name
def get_Team_Abbreviation(nba_teams, opposing_team):
    for team in nba_teams:
        abbreviation = ""
        if opposing_team == team['full_name']:
            #print(f"The opposing team the {opposing_team}'s abbreviation is {team['abbreviation']}")
            return team['abbreviation']


#gets the player stats for the regular season of a specific year
def getRegularSeasonStats(player_id, year):
    #print(f"{year} Season")
    game_log = playergamelog.PlayerGameLog(player_id=player_id, season=year, season_type_all_star='Regular Season')
    game_log_df = game_log.get_data_frames()[0]
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)
    #pd.set_option('display.width', None)
    #print(game_log_df)
    return game_log_df

def getRegularSeasonStatsWithRetry(player_id, year):
    return retry_api_call(getRegularSeasonStats, player_id, year)

#gets the column that contains every season a player has played and returns a list of all seasons played
def getAllSeasonsPlayed(player_id):
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career.get_data_frames()[0]
    list_of_years = career_df['SEASON_ID'].tolist()
    #print(list_of_years)
    return list_of_years
#calls the getRegularSeasonStats function as many times as the length of the career played and returns df with all seasons combined
def getEverySeason(player_id):
    combined_df = pd.DataFrame()
    years = getAllSeasonsPlayed(player_id)
    for year in years:
        game_log_df = getRegularSeasonStats(player_id, year)
        combined_df = pd.concat([combined_df, game_log_df], ignore_index=True)
        time.sleep(0.5)
    return combined_df
#takes in input of the number of games you want to track back and returns the stats from the last games played
def getLastPlayedGames(numberOfGames, game_log_df):
    numberOfGames = int(numberOfGames)
    #print(game_log_df[-numberOfGames:])
    last_played_games_df = game_log_df[:numberOfGames]
    return last_played_games_df
#returns a df with the stats against a specific opponent in a specific year
def getStatsVsSpecifcOpponent(opponent_abbreviation, game_log_df):
    specific_df = game_log_df[game_log_df['MATCHUP'].str.endswith(opponent_abbreviation)]
    #print(specific_df)
    return specific_df


































