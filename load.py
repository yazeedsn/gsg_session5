import os 
import pandas as pd 

def load_data(url: str, local_path: str) -> pd.DataFrame :
    if os.path.exists(local_path):
        print(f'Loading from cache: {local_path}')
        return pd.read_csv(local_path)
    print('Downloading from {url}...')
    df = pd.read_csv(url)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    df.to_csv(local_path)
    print(f'Save to {local_path}')
    return df