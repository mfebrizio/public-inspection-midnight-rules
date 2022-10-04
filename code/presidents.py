# import dependencies
import pandas as pd


def clean_president_column(df_input: pd.DataFrame, 
                            column: str = "president"):
    """Clean column containing president metadata for Federal Register API data.

    Args:
        df_input (pd.DataFrame): Input dataframe.
        column (str, optional): Column containing president metadata. Defaults to "president".

    Returns:
        DataFrame: Copy of df_input with new column, "president_id".
    """    
    # create deep copy of input dataframe
    df = df_input.copy(deep=True)
    
    # extract president identifier
    df["president_id"] = df.apply(lambda x: x[column]["identifier"], axis=1)
    president_list = list(set(df["president_id"].values.tolist()))
    print(", ".join(president_list))

    # return output df with new columns
    return df

