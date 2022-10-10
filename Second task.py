from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd


def prepare_dataset(delivery_area_id, orders, partners_delays):
    """
    Prepares dataset for training the classifier
    """
    orders_ = orders.loc[(orders['delivery_area_id'] == delivery_area_id)]
    delay_rate_ = partners_delays.loc[
        partners_delays['delivery_area_id'] == delivery_area_id]
    delay_rate_ = delay_rate_[delay_rate_['dttm'].isin(orders_['date_time'])]
    delay_rate_['orders_cnt'] = orders_['orders_cnt'].values
    delay_rate_['Target'] = (delay_rate_['delay_rate'] > 0.05).astype(int)
    delay_rate_.drop(['delivery_area_id'], axis=1,
                     inplace=True)
    X = delay_rate_.drop(['dttm', 'delay_rate', 'Target'], axis=1)
    y = delay_rate_['Target']
    return X, y


def training_classifier(X, y):
    """
    Preparation of logistic regression
    """
    model = LogisticRegression(C=0.1)
    model.fit(X, y)
    return model


def classifier_prep(delivery_area_id, orders, partners_delays):
    X, y = prepare_dataset(delivery_area_id, orders, partners_delays)
    return training_classifier(X, y)


def partner_cnt_det(model, orders_cnt):
    partner_cnt = 1
    x = pd.DataFrame({'partners_cnt': [partner_cnt],
                      'orders_cnt': [orders_cnt]})
    while model.predict(x)[0] == 1:
        partner_cnt += 1
        x = pd.DataFrame({'partners_cnt': [partner_cnt],
                          'orders_cnt': [orders_cnt]})
    return partner_cnt
