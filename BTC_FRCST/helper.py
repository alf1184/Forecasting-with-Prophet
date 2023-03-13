import pandas as pd
from datetime import datetime, date
import re
from pytrends import dailydata

def get_searches(kws, start_date, end_date):
    '''
    Takes a list of kew words and a time window
    and returns google searches associated with it
    as a DataFrame.
    '''
    dt_start = datetime.strptime(start_date, '%Y-%m-%d')
    dt_end = datetime.strptime(end_date, '%Y-%m-%d')
    start_year, start_month, start_day = dt_start.year, dt_start.month, dt_start.day
    end_year, end_month, end_day = dt_end.year, dt_end.month, dt_end.day
    
    d1 = date(start_year, start_month, start_day) 
    d2 = date(end_year, end_month, end_day)
    d = pd.date_range(d1, d2)
    df_trends = pd.DataFrame(index = d)
    
    for kw in kws:
        iot = dailydata.get_daily_data(kw, start_year, start_month, end_year, end_month, geo = 'US')
        iot = iot.drop(iot.columns[[0, 1, 2, 3]], axis = 1) # [0]: unscaled, [4]: scaled
        iot_columns = list(iot.columns.values)
        iot_columns_underscore = add_underscore(iot_columns)
        dict_name = dict(zip(iot_columns, iot_columns_underscore))
        iot = iot.rename(columns=dict_name)
        df_trends = pd.merge(df_trends, iot, left_index=True, right_index=True)
    return df_trends

def add_underscore(list):
    '''
    Takes a lists of spaced strings and returns them
    with underscores.
    '''
    list_underscore = []
    for item in list:
        item_underscore = re.sub('\ ', '_', item)
        list_underscore.append(item_underscore)
    return list_underscore

def drop_nans(df):
    print(df.loc[pd.isnull(df).any(1), :].index)
    null_posit = list(df.loc[pd.isnull(df).any(1), :].index)
    df = df.drop(index=null_posit)
    return df