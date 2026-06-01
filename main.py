from load import load_data
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