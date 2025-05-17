import dataCollection
import dataVisualization
import sqlDatabaseSetup
import unitTests


def main():
    sqlDatabaseSetup.databaseSetup()
    sqlDatabaseSetup.populateSeasonsTable()
    sqlDatabaseSetup.populateTeamsTable()
    sqlDatabaseSetup.populatePlayersTable()
    sqlDatabaseSetup.populateGameLogsTable()

    unitTests.test_seasons_populated()
    unitTests.test_teams_populated()
    unitTests.test_players_team_relation()
    unitTests.test_game_logs_relations()


    #first_name, last_name = input("Enter the player's full name (Ex: LeBron James): ").split(" ", 1)
    #opposing_team = input("Enter opposing team (Ex: Denver Nuggets): ")
    #print(f"You entered {first_name} {last_name}")
    #print(f"You entered the {opposing_team}")
    #nba_players = dataCollection.getAllActivePlayers()
    #nba_teams = dataCollection.getAllTeams()
    #player_id = dataCollection.get_ID(nba_players, first_name, last_name)
    #opposing_team_id = dataCollection.get_Team_ID(nba_teams, opposing_team)
    #opponent_abbreviation = dataCollection.get_Team_Abbreviation(nba_teams, opposing_team)
    #numberOfGames = input("How many games do you want for recent history? Enter a integer: ")
    #stat = input("Enter the stat for the betting line (Ex: PTS for points): ")
    #betting_line = float(input("Enter the betting line for the stat (Ex: 20.0): "))
    #dataVisualization.plotStatsVsSpecificOpponentBarGraph(dataCollection.getStatsVsSpecifcOpponent(opponent_abbreviation, dataCollection.getEverySeason(player_id)), stat, betting_line)
    



if __name__ == "__main__":
    main()


