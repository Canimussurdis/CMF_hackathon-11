import pandas as pd
import numpy as np
from prophet import Prophet


def preprocessing(df):
    """
    Prepares dataset for processing for prediction
    """
    df_['date_only'] = pd.to_datetime(df['date']).dt.date
    df_['hour'] = pd.to_datetime(df['date']).dt.hour

    return df_


def fill_with_zeroes(df, working_hours):
    """
    Fills missing values with zeroes in the orders dataframe  
    """
    delivery_area_id = df['delivery_area_id'].iloc[0]
    start = pd.to_datetime(
        working_hours[working_hours['delivery_area_id'] == delivery_area_id][
            'start']).dt.hour.iloc[0]
    end = pd.to_datetime(
        working_hours[working_hours['delivery_area_id'] ==\
                      delivery_area_id]['end']).dt.hour.iloc[0]
    df_ = pd.DataFrame([])
    df_['hour'] = np.arange(start, end+1)
    date = df['date_only'].iloc[0]
    df_['date_only'] = date
    df_['delivery_area_id'] = delivery_area_id
    df_['orders_cnt'] = 0
    df_['date'] = [pd.Timestamp(date.year,
                                date.month,
                                date.day, h) for h in np.arange(start, end+1)]
    for hour in np.arange(start, end+1):
        if hour in df['hour'].values:
            df_.loc[df_['hour'] == hour, 'orders_cnt'] =\
                 df.loc[df['hour'] == hour, 'orders_cnt'].iloc[0]

    df_ = df_[['delivery_area_id', 'date', 'orders_cnt', 'date_only', 'hour']]
    df_ = df_.sort_values('date')
    
    return df_


def prepare_Prophet_model(df_train):
    """
    Prepares Prophet
    """
    model = Prophet(daily_seasonality=True,
                    yearly_seasonality=True,
                    changepoint_prior_scale=0.001)
    model.fit(df_train)
    return model


def create_df_dates(start, end):
    """
    Creates DataFrame with dates for prediction
    """
    start_ = pd.to_datetime(start)
    end_ = pd.to_datetime(end)
    df_ = pd.DataFrame()
    df_['ds'] = pd.date_range(start_, end_)
    return df_


def make_predictions(df_dates, model):
    """
    Calculates df with predictions
    """
    predictions = model.predict(df_dates)
    return predictions
