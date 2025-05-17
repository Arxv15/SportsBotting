import matplotlib.pyplot as plt
import seaborn as sns

#plots a graph that compares a specific stat against a betting line vs a specific opponent
def plotStatsVsSpecificOpponentBarGraph(specific_df, stat, betting_line):
    colors = ['green' if value > betting_line else 'red' if value < betting_line else 'grey' for value in specific_df[stat]]
    plt.figure(figsize=(12, 6))
    plt.bar(specific_df['GAME_DATE'], specific_df[stat], color=colors)
    plt.xlabel("Game Date")
    plt.ylabel(stat)
    plt.title(f"{stat} per Game")
    plt.axhline(y=betting_line, color='black', linestyle='--', label=f"Betting Line ({betting_line})")
    plt.legend()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()