############# DEPENDENCIES ##############

import numpy as np
import pandas as pd

############# TOOLS FOR EXAMINING DATA FRAMES ##############

def info_frame(df):
    
    """
    Given a DataFrame, gets the name, type, and number of NaN values for each column and stores this information in a new DataFrame.
    """

    info = pd.DataFrame([[col, df[col].dtype, df[col].isna().sum()] for col in df],
                       columns=['name', 'type', 'num_nans'])

    return info

def count_nan(df):
    
    """
    Given a DataFrame, gets the name of each column and the number of NaN values in it.
    Returns this information in a new DataFrame, sorted by number of NaN values.
    Leaves out any columns that have no NaN values.
    If no NaN values found, returns an empty DataFrame.
    """
    
    null_counts = df.isna().sum().sort_values(ascending=False)
    i = 0
    if null_counts[i] == 0:
        return pd.DataFrame(None)
    while i < len(null_counts):
        if null_counts[i] != 0:
            i += 1
        else:
            return pd.DataFrame(zip(null_counts.index[:i], null_counts[:i]))
    return pd.DataFrame(zip(null_counts.index[:i], null_counts[:i]))

def find_non_numeric(in_col):
    
    """
    Finds each unique entry in an iterable that cannot be typecast as float and returns a list of those entries.
    """
    
    non_nums = []
    for item in in_col:
        try:
            float(item)
        except:
            if item not in non_nums:
                non_nums.append(item)
    return non_nums

############# TOOLS FOR MODIFYING DATA FRAMES ##############

def df_cols_to_snake_case(df):
    
    """
    Given a DataFrame, converts column titles from separate words to snake_case.
    Will not work on CamelCase.
    """
    
    return df.rename(mapper={col : col.lower().replace(' ', '_') for col in df.columns}, axis=1)

def convert_to_float(in_item, non_numeric_fill=np.nan):
    
    """
    Converts any input that can be typecast as numeric input to a float.
    non_numeric_fill specifies what to return if the input cannot be cast as float.  Default np.nan.
    """
    
    try:
        return float(in_item)
    except:
        return non_numeric_fill