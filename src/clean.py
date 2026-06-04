import pandas as pd

def clean_chess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=['Unnamed: 0'])
    df[['time_base', 'time_inc']] = df['time_increment'].str.split('+', expand=True).astype(int)
    df['rating_diff'] = df['white_rating'] - df['black_rating']
    df['opening_family'] = df['opening_fullname'].str.split(':').str[0].str.strip().astype(str)
    df = df.drop(columns=['opening_response'])
    df['is_suspicious'] = df['turns'] < 5
    assert df['rating_diff'].notna().all()
    assert df.duplicated().sum() == 0
    return df

