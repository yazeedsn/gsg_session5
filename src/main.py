from load import load_data
from fetch_and_clean import fetch_and_clean_chess
from util import info_to_markdown

import pandas as pd
import matplotlib.pyplot as plt
import os 

# meta data
CHESS_URL = 'https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view'
PLAYERS_URL = 'https://drive.google.com/file/d/1wCSAkGagMzWiToedLC3ZGo_lGf_laF-k/view'

CHESS_URL='https://drive.google.com/uc?id=' + CHESS_URL.split('/')[-2]
PLAYERS_URL='https://drive.google.com/uc?id=' + PLAYERS_URL.split('/')[-2]

# data loading
path_rdata = 'data/raw/'
df_chess = load_data(CHESS_URL, os.path.join(path_rdata, 'chess_games.csv'))
df_players = load_data(PLAYERS_URL, os.path.join(path_rdata, 'players_registry.csv'))


# readme file handling
readme = open('README.md', 'w')
readme.write("""---
title: Analysis of Chess Game and Player Data
description: Creating a clean pipline for data analysis of chess games and players from chess data.
author: Yazid Abusultan
---\n""")
readme.write('# GSG PSSAR Advanced Course Session 5\n')
readme.write('## Data Quality Report\n\n')

# Exploration
print(df_chess.head())
print(df_chess.info())

readme.write(f'### Chess Games Data \n\n')
readme.write(f'#### Raw Data \n')
readme.write(info_to_markdown(df_chess))

print('------------------------- Setup Questions --------------------------')
chess_rows = df_chess.shape[0]
chess_drows = df_chess.duplicated().sum()
readme.write(f'\n**Chess games dataframe has {chess_drows} duplicated rows out of {chess_rows}**\n')

print(f'# rows = {chess_rows}')
print(f'# duplicated rows = {chess_drows}')
print(f'# duplicated move sequence = {df_chess['moves'].duplicated().sum()}')
print(f'% missing opening_response = {100*df_chess['opening_response'].isna().sum() / len(df_chess['opening_response'])}')
print(f'% missing opening_variation = {100*df_chess['opening_variation'].isna().sum() / len(df_chess['opening_variation'])}')
print(f'min number of turns = {df_chess['turns'].min()}')


# Cleaning
df_chess = fetch_and_clean_chess(df_chess, os.path.join(path_rdata, 'chess_games.csv'))
readme.write(f'\n### Cleaned Data \n')
readme.write(info_to_markdown(df_chess))
print(df_chess)

readme.write("\n#### Important Changes:\n")
readme.write("* Removed 'Unnamed: 0' since it does not serve a purpose and game_id can be used as an index instead.\n")
readme.write("* Removed opening_response since it is mostly nulls.\n")
readme.write("* Splited time_increment into time base and time increment for cleaner time view.\n")
readme.write("* Added a rating difference column to highlight the difference between the two players of any game.\n")
readme.write("* Extracted an opening family column to group openings within each family.\n")
readme.write("* Added is_suspicious column to detect fake games (eg. a player won after 1 turn in the game).\n")

# Stage 3
print('------------------------- Analytical Questions --------------------------')

rates = df_chess.groupby(['winner']).size() / len(df_chess) * 100
most_common_status = df_chess.groupby(['victory_status']).size().idxmax()
highest_avg_terms = df_chess.groupby(['victory_status'])['turns'].mean().idxmax()
popular_family_black = df_chess[df_chess['winner'] == 'Black'].groupby('opening_family').size().idxmax()
popular_family_white = df_chess[df_chess['winner'] == 'White'].groupby('opening_family').size().idxmax()
rated_games_white_win_rate = df_chess[df_chess['rated']].groupby('winner').size()['White'] / len(df_chess[df_chess['rated']]) * 100
unrated_games_white_win_rate = df_chess[~df_chess['rated']].groupby('winner').size()['White'] / len(df_chess[~df_chess['rated']]) * 100

readme.write('\n### Analytics Outcomes\n\n')
readme.write('Win Rates\n')
readme.write(f'{rates.to_markdown()}\n\n')
readme.write(f'Most common victory status is {most_common_status} \n\n')




# plot hist to decide turns class boundaries
# df_chess.hist(column='turns', bins=50)
# plt.show()

readme.write(f'Games were classed into Short, Medium, Long based on the histogram of turn counts.\n Medium Games are between 30 to 70 turns since the majority of games fall into that range.\n')
def classify(x: int) -> str:
    if x <= 30: return 'Short'
    elif x <= 70: return 'Medium'
    else: return 'Long'


df_chess['duration'] = df_chess['turns'].apply(classify)
durations_rate = df_chess.groupby(['duration']).size() / len(df_chess) * 100


print(f"The rate for Draw, White, or Black is {rates}")
print(f'Most games end with {most_common_status}')
print(f"{highest_avg_terms} has the highest avarge number of turns")
print(f"The most popular family when Black wins is {popular_family_black}")
print(f"The most popular family when White wins is {popular_family_white}")
print(f"Rated games White win rate {rated_games_white_win_rate}")
print(f"Unrated games White win rate {unrated_games_white_win_rate}")
print(f"% of Duration classes {durations_rate}")

#Stage 4
readme.write(f'\n### Players Registry Data \n\n')
readme.write(f'#### Raw Data \n')
readme.write(info_to_markdown(df_players))
players_drows = df_players.duplicated().sum()
readme.write(f'\nPlayers registry has {chess_drows} duplicated rows\n')


print(df_players.head())
print(df_players.info())

df_merged = pd.merge(
    df_chess[['game_id', 'white_id', 'white_rating', 'winner']],
    df_players.rename(columns={'username': 'white_id'}),
    on= 'white_id',
)

readme.write(f'\n### Merged Data \n\n')
readme.write(f'**Merged chess games and players registry dataframes.**\n')
readme.write(info_to_markdown(df_merged))

print(df_merged.columns)
print(df_merged.head())
num_players_unregistered = len(df_chess['white_id'].unique()) - len(df_merged['white_id'].unique())
readme.write(f'\n**There are {len(df_merged['white_id'].unique())} registered players and {num_players_unregistered} unregistered ones.**\n\n')

countries_before_cleaning = df_merged['country'].unique()
country_map = {
    'US': 'United States',
    'USA': 'United States',
    'united states': 'United States',
    'RUS': 'Russia',
    'russian federation': 'Russia',
    'UA': 'Ukraine',
    'UK': 'United Kingdom',
    'united kingdom': 'United Kingdom',
    'GB': 'United Kingdom',
    'BRA': 'Brazil',
    'brazil': 'Brazil',
    'PL': 'Poland',
    'poland': 'Poland',
    'france': 'France',
    'FR': 'France',
    'DE': 'Germany',
    'Deutschland': 'Germany',
    'IN': 'India',
    'ES': 'Spain'
    }



print(f'# white players without a registery: {num_players_unregistered}')

df_merged['country'] = df_merged['country'].map(country_map).fillna(df_merged['country'])
countries = df_merged['country'].dropna().sort_values(ascending=True).unique()
print(f"# countries after cleaning: {countries.size}")
readme.write(f'Registered players join from the following countries\n')
for c in countries:
    readme.write(f'* {c}\n')



df_chess.groupby('winner').size().plot(kind='bar')
os.makedirs('output', exist_ok=True)
plt.savefig('output/wins_by_color.png')
plt.show()

df_chess[df_chess['rated']].plot(kind='scatter', x='white_rating', y='turns')
plt.savefig('output/rate_to_turn.png')
plt.show()

print(df_chess.groupby('victory_status')['turns'].sum())
df_chess.boxplot(column='turns', by='victory_status')
plt.savefig('output/turn_by_victory_status.png')
plt.show()

readme.close()