import pandas as pd

def condense(df, col):
    one_df = df[[col]]
    indices = df.index.names
    summed = one_df.groupby(level=indices).sum()
    df.reset_index(inplace=True)
    df.drop_duplicates(indices, inplace=True)
    df.set_index(indices, inplace=True)
    df[col] = summed[col]
    return df
