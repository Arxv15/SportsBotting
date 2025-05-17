import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///nba_data.db')
connection = engine.connect()

def test_seasons_populated():
    result = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM seasons"))
    count = result.scalar()
    assert count > 0, "Seasons table is empty!"
    print(f"Seasons table row count: {count}")

def test_teams_populated():
    result = connection.execute(sqlalchemy.text("SELECT COUNT(*) FROM teams"))
    count = result.scalar()
    assert count > 0, "Teams table is empty!"
    print(f"Teams table row count: {count}")

def test_players_team_relation():
    query = """
    SELECT COUNT(*) FROM players p
    LEFT JOIN teams t ON p.team_id = t.team_id
    WHERE p.team_id IS NOT NULL AND t.team_id IS NULL
    """
    result = connection.execute(sqlalchemy.text(query))
    count = result.scalar()
    assert count == 0, "There are players with invalid team_id references!"
    print("All player team_ids reference valid teams.")

def test_game_logs_relations():
    query = """
    SELECT COUNT(*) FROM game_logs g
    LEFT JOIN players p ON g.player_id = p.player_id
    LEFT JOIN seasons s ON g.season_id = s.season_id
    LEFT JOIN teams t1 ON g.team_id = t1.team_id
    LEFT JOIN teams t2 ON g.opp_team_id = t2.team_id
    WHERE p.player_id IS NULL
    OR s.season_id IS NULL
    OR t1.team_id IS NULL
    OR t2.team_id IS NULL
    """
    result = connection.execute(sqlalchemy.text(query))
    count = result.scalar()
    assert count == 0, "Some game_logs have invalid foreign key references!"
    print("All game_logs foreign keys are valid.")
    
