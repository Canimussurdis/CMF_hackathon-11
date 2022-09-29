# Файл, в который можно складывать код для написания всех фичей
import pandas as pd
import numpy as np


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
    df['date_without_time'] = pd.to_datetime(df['date']).dt.date
    df_proc = df.groupby(['delivery_area_id', 'date_without_time'])
    df_proc = df_proc['orders_cnt'].apply(np.sum).reset_index()
    return df_proc
