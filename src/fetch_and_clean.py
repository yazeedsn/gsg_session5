from fetch_and_pipe import fetch_and_pipe
from clean import clean_chess
import pandas as pd 
import os 

def fetch_and_clean_chess(url: str, local_path: str) -> pd.DataFrame:
    df = fetch_and_pipe(url, local_path, clean_chess)
    os.makedirs('data/processed/', exist_ok=True)
    df.to_csv('data/processed/chess_cleaned.csv')
    return df