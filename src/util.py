import pandas as pd 

def info_to_markdown(df: pd.DataFrame) -> str:
    info_df = pd.DataFrame({
        "Column": df.columns,
        "Non-Null Count": df.notnull().sum().values,
        "Data Type": df.dtypes.astype(str).values
    })
    return info_df.to_markdown(index=False) + '\n'