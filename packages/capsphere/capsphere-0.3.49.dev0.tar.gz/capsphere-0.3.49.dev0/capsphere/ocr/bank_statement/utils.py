import pandas as pd


def __format_column(df_column: pd.Series) -> pd.Series:
    return df_column.str.replace(',', '').replace('', '0.00')
