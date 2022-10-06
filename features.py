# Файл, в который можно складывать код для написания всех фичей
import pandas as pd
import numpy as np
from fastai.tabular.core import add_datepart
import holidays_class
import config 
import datetime


def daily_order_counts(orders):
    """
    Calculates daily order counts for every delivery area
     Arguments:
     Orders - dataframe with delivery area identifier, date and time,
                   and order counts for every hour
     Returns:
      Dataframe with delivery area identifier, date, and sum of orders during
        one day
    """
    df = orders.copy()
    df['date'] = pd.to_datetime(df['date']).dt.date
    df_proc = df.groupby(['delivery_area_id', 'date'])
    df_proc = df_proc['orders_cnt'].apply(np.sum).reset_index()
    return df_proc

def weekly_orders_count(orders):
    """
    Calculates daily order counts for every delivery area
     Arguments:
     Orders - dataframe with delivery area identifier, date and time,
                   and order counts for every hour
     Returns:
      Dataframe with delivery area identifier, date, and sum of orders during
        one day
    """
    df = orders.copy()
    df.loc[:, 'date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    df.loc[:, 'week'] = df['date'].dt.week
    grouped_df = df.groupby(['delivery_area_id', 'week']).agg({'orders_cnt':'sum'}).reset_index()
    return grouped_df


def date_features(df):
    """
    Calculates date features such as month, day of week,
        Argument:
            df - dataframe with dates, delivery areas id, and order counts
        Return
            df_proc - dataframe with dates, delivery areas id, order counts,
            and date features Month, Day, Dayofweek, Is_month_end,
            Is_month_start, Is_quarter_end,	Is_quarter_start
    """
    df_proc = df.copy()
    add_datepart(df_proc, 'date', drop=False)
    df_proc.drop(['Year', 'Dayofyear', 'Elapsed', 'Is_year_end',
                  'Is_year_start', 'Week'],
                 axis=1,
                inplace=True)
    df_proc['Is_month_end'] = df_proc['Is_month_end'].astype(int)
    df_proc['Is_month_start'] = df_proc['Is_month_start'].astype(int)
    df_proc['Is_quarter_end'] = df_proc['Is_quarter_end'].astype(int)
    df_proc['Is_quarter_start'] = df_proc['Is_quarter_start'].astype(int)
    return df_proc

def add_holidays(data, max_year):
    '''
    Create binary columns with holidays and merge it with original dataframe

    Parametrs
    ---------
    data : pd.DataFrame, with previous feature engineering processing
    
    max_year : int, maximum year from our DataFrame
    '''
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

    # Таблица, с бинарными колонками праздников из holiday_class
    binary_holiday_df = holidays_class.SpecialEvents(df=data, date_col='date').holidays_dummies_df(max_year=max_year+1)

    # Присоединим полученную таблицу к нашим данным
    data = data.merge(
        binary_holiday_df, 
        how='left', 
        left_on=data['date'].dt.date, 
        right_on=binary_holiday_df['date'].dt.date)

    # Удалим ненужные колонки 
    data.drop(columns=['date_y', 'key_0', 'total_holidays'], inplace=True)
    data.rename(columns={'date_x':'date'}, inplace=True)
    data.fillna(0, inplace=True)
            
    return data

def add_eve(data):
    '''
    Creates new columns which represents eve days for several holidays in binary format

    Parametrs
    ---------
    data : pd.DataFrame, datagrame with previous feature engineering preprocessing
    '''
    # Sort dataframe on date_time column
    data.sort_values(by='date', inplace=True)
    
    hol_with_eve = config.HOLIDAYS_WITH_EVE
    one_day_eve = config.ONE_DAY_EVE

    for column in hol_with_eve:

        eve_dates = [] # Список дат канунов
        eve_shift = 1 if column in one_day_eve else 2 # Определяет сколько канунов нужно добавить 
        hol_dates = data[data[column] == 1]['date'].dt.date.unique() # Праздничные даты у каждого праздника

        # Итерируемся по каждой праздничной дате 
        for hol_date in hol_dates:

            # Итерируемся по каждому числу в сдвиге и добавляем кануны 
            for shift in range(1, eve_shift+1):
                eve_dates.append(hol_date + datetime.timedelta(days=-shift))
        
        data.loc[:, 'EVE_' + column[4:]] = data['date'].apply(lambda x: 1 if x.date() in eve_dates else 0)
    
    return data



