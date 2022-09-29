# Файл, в который можно складывать код для написания всех фичей
import pandas as pd
import numpy as np
from fastai.tabular.core import add_datepart


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


def date_features(df):
    """
    Calculates date features such as month, day of week,
        Argument:
            df - dataframe with dates, delivery areas id, and order counts
        Return
            df_proc - dataframe with dates, delivery areas id, order counts,
            and date features Month, Day, Dayofweek, Is_month_end, Is_month_start,
            Is_quarter_end,	Is_quarter_start
    """
    df_proc = df.copy()
    add_datepart(df_proc, 'date', drop=False)
    df_proc.drop(['Year', 'Dayofyear', 'Elapsed', 'Is_year_end', 'Is_year_start', 'Week'],
             axis=1,
             inplace=True)
    df_proc['Is_month_end'] = df_proc['Is_month_end'].astype(int)
    df_proc['Is_month_start'] = df_proc['Is_month_start'].astype(int)
    df_proc['Is_quarter_end'] = df_proc['Is_quarter_end'].astype(int)
    df_proc['Is_quarter_start'] = df_proc['Is_quarter_start'].astype(int)
    return df_proc

