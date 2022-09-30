import pandas as pd
import features as f
import models
from models import GroupTimeSeriesSplit
from lightgbm import LGBMRegressor


orders = pd.read_csv('orders.csv')
orders['date'] = pd.to_datetime(orders['date'])

data = f.daily_order_counts(orders)
data = f.date_features(data)
data_with_targets = data.groupby('delivery_area_id').apply(f.target_generation)
data_with_targets = data_with_targets.reset_index(drop=True)

params = []
for i in range(7):
    params += [{
            'num_leaves': 300,
            'n_estimators': 100,
            'max_bin': 5,
            'learning_rate': 0.1,
    }]
model = []

for p in params:
    model += [LGBMRegressor(**p)]

date_test = pd.to_datetime('2021-11-01')
data_train = data_with_targets.loc[data_with_targets['date'] < date_test]
data_test = data_with_targets.loc[data_with_targets['date'] >= date_test]

y_train = data_train[['Target_{}'.format(i) for i in range(7)]]
X_train = data_train.drop(['date'], axis=1)

X_test = data_test.drop(['date'], axis=1)

model_trained = models.fit(model, X_train, y_train)
y_pred = models.predict(model, X_test)
