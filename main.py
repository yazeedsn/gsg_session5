from load import load_data
from clean import clean_chess

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

# Exploration
print(df_chess.head())
print(df_chess.info())


print('------------------------- Setup Questions --------------------------')
print(f'# rows = {df_chess.shape[0]}')
print(f'# duplicated rows = {df_chess.duplicated().sum()}')
print(f'# duplicated move sequence = {df_chess['moves'].duplicated().sum()}')
print(f'% missing opening_response = {100*df_chess['opening_response'].isna().sum() / len(df_chess['opening_response'])}')
print(f'% missing opening_variation = {100*df_chess['opening_variation'].isna().sum() / len(df_chess['opening_variation'])}')
print(f'min number of turns = {df_chess['turns'].min()}')


# Cleaning
df_chess = clean_chess(df_chess)
print(df_chess)

# Stage 3
print('------------------------- Analytical Questions --------------------------')

rates = df_chess.groupby(['winner']).size() / len(df_chess) * 100
most_common_status = df_chess.groupby(['victory_status']).size().idxmax()
highest_avg_terms = df_chess.groupby(['victory_status'])['turns'].mean().idxmax()
popular_family_black = df_chess[df_chess['winner'] == 'Black'].groupby('opening_family').size().idxmax()
popular_family_white = df_chess[df_chess['winner'] == 'White'].groupby('opening_family').size().idxmax()
rated_games_white_win_rate = df_chess[df_chess['rated']].groupby('winner').size()['White'] / len(df_chess[df_chess['rated']]) * 100
unrated_games_white_win_rate = df_chess[~df_chess['rated']].groupby('winner').size()['White'] / len(df_chess[~df_chess['rated']]) * 100

# plot hist to decide turns class boundaries
df_chess.hist(column='turns', bins=50)
plt.show()

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
