from load import load_data
import pandas as pd

def fetch_and_pipe(url: str, local_path: str, pipe: callable | list[callable]) -> pd.DataFrame:
    df = load_data(url, local_path)
    if callable(pipe):
        df = pipe(df)
        assert isinstance(df, pd.DataFrame)
        return df
    for fn in pipe:
        df = fn(df)
    assert isinstance(df, pd.DataFrame)
    return df