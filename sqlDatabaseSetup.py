import sqlalchemy
import dataCollection
import time


engine = sqlalchemy.create_engine('sqlite:///nba_data.db', echo=True)
metadata = sqlalchemy.MetaData()

seasons = sqlalchemy.Table(
    'seasons',
    metadata,
    sqlalchemy.Column('season_id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('start_year', sqlalchemy.Integer),
    sqlalchemy.Column('end_year', sqlalchemy.Integer)
    )

teams = sqlalchemy.Table(
    'teams',
    metadata,
    sqlalchemy.Column('team_id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('abbreviation', sqlalchemy.String),
    sqlalchemy.Column('full_name', sqlalchemy.String)
)

players = sqlalchemy.Table(
    'players',
    metadata,
    sqlalchemy.Column('player_id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('full_name', sqlalchemy.String),
    sqlalchemy.Column('team_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('teams.team_id'))
)

game_logs = sqlalchemy.Table(
    'game_logs',
    metadata,
    sqlalchemy.Column('game_id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('player_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('players.player_id')),
    sqlalchemy.Column('season_id', sqlalchemy.String, sqlalchemy.ForeignKey('seasons.season_id')),
    sqlalchemy.Column('game_date', sqlalchemy.String),
    sqlalchemy.Column('matchup', sqlalchemy.String),
    sqlalchemy.Column('pts', sqlalchemy.Integer),
    sqlalchemy.Column('ast', sqlalchemy.Integer),
    sqlalchemy.Column('reb', sqlalchemy.Integer),
    sqlalchemy.Column('team_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('teams.team_id')),
    sqlalchemy.Column('opp_team_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('teams.team_id'))
)

def databaseSetup():
    metadata.create_all(engine)

def populateSeasonsTable():
    current_season = dataCollection.getCurrentRegularSeasonDate()
    current_start_year = int(current_season.split("-")[0])

    seasons_list = []
    for year in range(2003, current_start_year + 1): #filling the table with every year from the oldest player in the league's draft date until the present
        season_id = f"{year}-{str(year + 1)[2:]}"
        seasons_list.append({
            "season_id" : season_id,
            "start_year" : year,
            "end_year" : year + 1
        })
    with engine.connect() as connect:
        for season in seasons_list:
            statement = sqlalchemy.insert(seasons).values(**season).prefix_with("OR IGNORE")
            connect.execute(statement)
        connect.commit()

def populateTeamsTable():
    nba_teams = dataCollection.getAllTeams()
    with engine.connect() as connect:
        for team in nba_teams:
            statement = sqlalchemy.insert(teams).values(
                team_id = team['id'],
                abbreviation = team['abbreviation'],
                full_name = team['full_name']
            ).prefix_with("OR IGNORE")
            connect.execute(statement)
        connect.commit()

def populatePlayersTable():
    active_players = dataCollection.getAllActivePlayers()
    with engine.connect() as connect:
        for player in active_players:
            team_id = dataCollection.get_player_team_id(player['id'])
            statement = sqlalchemy.insert(players).values(
                player_id = player['id'],
                full_name = player['full_name'],
                team_id = team_id
            ).prefix_with("OR IGNORE")
            connect.execute(statement)
            time.sleep(0.5)
        connect.commit()

def populateGameLogsTable():
    active_players = dataCollection.getAllActivePlayers()
    teams = dataCollection.getAllTeams()
    for player in active_players:
        player_id = player['id']
        seasons = dataCollection.getAllSeasonsPlayed(player_id)
        time.sleep(1.5)
        for season in seasons:
            time.sleep(30)
            game_log = dataCollection.getRegularSeasonStatsWithRetry(player_id, season)
            for _, row in game_log.iterrows():
                matchup = row['MATCHUP']
                if " vs. " in matchup:
                    opp = matchup.split("vs. ")[-1]
                    team = matchup.split(" ")[0]
                else:
                    opp = matchup.split("@ ")[-1]
                    team = matchup.split(" ")[0]

                team_name = dataCollection.get_Full_Name_From_Abbreviation(teams, team)
                opp_team_name = dataCollection.get_Full_Name_From_Abbreviation(teams, opp)
                team_id = dataCollection.get_Team_ID_From_Full_Name(teams, team_name)
                opp_team_id = dataCollection.get_Team_ID_From_Full_Name(teams, opp_team_name)
                statement = sqlalchemy.insert(game_logs).values(
                    game_id = row['Game_ID'],
                    player_id = player_id,
                    season_id = season,
                    game_date = row['GAME_DATE'],
                    matchup = matchup,
                    pts = row['PTS'],
                    ast = row['AST'],
                    reb = row['REB'],
                    team_id = team_id,
                    opp_team_id = opp_team_id
                ).prefix_with("OR IGNORE")

                with engine.connect() as connect:
                    connect.execute(statement)
                    connect.commit()
                time.sleep(0.5)
        time.sleep(30)

