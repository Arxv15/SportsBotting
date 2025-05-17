import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def construct_NBAplayer_url(first_name, last_name, year, num):
    url = f'https://www.basketball-reference.com/players/{last_name[0].lower()}/{last_name[:5].lower()}{first_name[:2].lower()}{num}/gamelog/{year}'
    return url

def construct_NFLplayer_url(first_name, last_name, year, num):
    url = f'https://www.pro-football-reference.com/players/{last_name[0].upper()}/{last_name[:4].title()}{first_name[:2].title()}00/gamelog/{year}/'
    return url


def scrape_NBAgame_log(player_url):
    response = requests.get(player_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', {'id': 'pgl_basic'})
    headers = [th.getText() for th in table.find('thead').findAll('th')]
    
    rows = table.find('tbody').findAll('tr', {'class': None})
    NBAgame_data = []
    for row in rows:
        cols = row.findAll('td')
        NBAgame_data.append([col.getText() for col in cols])
    
    return pd.DataFrame(NBAgame_data, columns=headers[1:])





def plot_NBAbar_graphs(df, stat, betting_line, opponent):
    df[stat] = pd.to_numeric(df[stat], errors='coerce')
    last_10_games = df.tail(10)
    
    fig, ax = plt.subplots(2, 1, figsize=(12, 10))
    
    
    ax[0].bar(last_10_games['Date'], last_10_games[stat], color='b', label=stat)
    ax[0].axhline(betting_line, color='r', linestyle='--', label='Betting Line')
    ax[0].set_title(f'Last 10 Games - {stat}')
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel(stat)
    ax[0].legend()
    
    last_10_vs_opponent = df[df['Opp'] == opponent].tail(10)
    
    ax[1].bar(last_10_vs_opponent['Date'], last_10_vs_opponent[stat], color='g', label=stat)
    ax[1].axhline(betting_line, color='r', linestyle='--', label='Betting Line')
    ax[1].set_title(f'Last 10 Games vs {opponent} - {stat}')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel(stat)
    ax[1].legend()
    
    plt.tight_layout()
    plt.show()




# Get user inputs
sport = input("Enter sport you are betting on: ")

if sport == 'basketball' or sport == 'Basketball':
    first_name = input("Enter the player's first name: ")
    last_name = input("Enter the player's last name: ")
    year = input("Enter the year: ")
    num = input("Enter the number behind the name on website basketballreference: ")
    stat = input("Enter the statistic to analyze (e.g., 'PTS' for points, 'AST' for assists): ")
    betting_line = float(input("Enter the betting line for the statistic (e.g., 30.5 *has to be a decimal): "))
    opponent = input("Enter the opposing team's abbreviation (e.g., 'LAC' for Los Angeles Clippers): ")

    NBAplayer_url = construct_NBAplayer_url(first_name, last_name, year, num)
    NBAdf = scrape_NBAgame_log(NBAplayer_url)
    plot_NBAbar_graphs(NBAdf, stat, betting_line, opponent)





