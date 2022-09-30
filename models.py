import pandas as pd
import numpy as np
import lightgbm


def target_generation(df):
    """
    Creates dataframe with generated targets - daily order counts
    for next 7 days
    Arguments:
        df - Dataframe with column 'orders_cnt' for given delivery area
    Returns:
        Dataframe with columns with target variables
    """
    df_ = df.copy()
    for i in range(0, 7):
        df_['Target_{}'.format(i)] = df_['orders_cnt'].shift(-i-1)
    df_.dropna(inplace=True)
    for i in range(0, 7):
        df_['Target_{}'.format(i)] = df_['Target_{}'.format(i)].astype(int)
    return df_


def fit(model, X, y):
    """
    Function for training the set of LGBM regressors
    Arguments:
        model - list of LGBM regressors
        X - dataframe with features from training set
        y - dataframe with target variables
    Returns:
        model - list of trained LGBM regressors
    """
    for i in range(0, 7):
        model[i].fit(X, y['Target_{}'.format(i)])
    return model


def predict(model, X_test):
    """
    Functions calculate the target variables
    Arguments:
        model - list of trained LGBM regressors
        X - dataframe with features from the test set
    Returns:
        y_pred - dataframe with predicted target variables
    """
    y_pred = pd.DataFrame([])
    for i in range(0, 7):
        y_pred['Target_{}'.format(i)] = model[i].predict(X_test)
        y_pred['Target_{}'.format(i)] = y_pred['Target_{}'.format(i)].astype(
            int)
    return y_pred
