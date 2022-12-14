# -*- coding: utf-8 -*-
"""Second Task.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HsOH10aQG3nFwjKL_hSNzEQcMoG_2a6y
"""

# Установка LightGBM и Optuna - библиотеки для подбора гиперпараметров
!pip install lightgbm optuna
from lightgbm import LGBMRegressor
import optuna
import matplotlib.pyplot as plt
import warnings
import pandas as pd
import numpy as np
warnings.filterwarnings("ignore")

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/Financial\ Modeling/CMF/Хакатон\ от\ Сбера
!pwd

orders = pd.read_csv('orders.csv')
orders['date'] = pd.to_datetime(orders['date'])
partners_delays = pd.read_csv('partners_delays.csv')
partners_delays['dttm'] = pd.to_datetime(partners_delays['dttm'])
clusters = pd.read_excel('standard_scaler_clustering.xlsx')
partners_delays

orders

clusters.columns = ['delivery_area_id', 'cluster']
clusters

plt.yscale('log')
plt.hist(partners_delays['delay_rate'])

import features as f

orders = f.daily_order_counts(orders)

partners_delays['hour'] = partners_delays['dttm'].dt.hour
partners_delays['date'] = partners_delays['dttm'].dt.date
partners_delays

# partners_delays['daily_order_counts'
data = pd.merge(partners_delays, orders[['delivery_area_id', 'date', 'orders_cnt']],
         on=['delivery_area_id', 'date'], how='left')
# partners_delays['daily_order_counts'
data = pd.merge(data, clusters, on=['delivery_area_id'], how='left')

data

data = f.date_features(data)
data

X = data.drop(['dttm','date','Month','Week','delay_rate'], axis=1)
y = data['delay_rate']

"""# Тренировка модели"""

# Разбиение на тренировочный, валидационный и тестовый наборы
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Функция для определения гиперпараметров
def objectives(trial):
    params = {
            'num_leaves': trial.suggest_int('num_leaves', 300, 4000),
            'n_estimators': trial.suggest_int('n_estimators', 10, 1000),
            'max_bin': trial.suggest_int('max_bin', 2, 100),
            'learning_rate': trial.suggest_uniform('learning_rate',0, .1),
    }

    model = LGBMRegressor(**params)
    model.fit(X_train,y_train)
    score = model.score(X_val,y_val) #r2_score
    return score

# Поиск наилучшего набора гиперпараметров
opt = optuna.create_study(direction='maximize',
                          sampler=optuna.samplers.RandomSampler(seed=0))
opt.optimize(objectives, n_trials=20)

# Набор гиперпараметров с лучшим результатом на валидации 
trial = opt.best_trial
params_best = dict(trial.params.items())
params_best['random_seed'] = 42
    
# Предсказание с оптимальными гиперпараметрами на тестовой выборке
model_o = LGBMRegressor(**params_best)
model_o.fit(X_train, y_train)
print('Коэффициент детерминации на тестовой выборке:')
model_o.score(X_test, y_test)

# График с распределением feature importance
feature_importances = (model_o.feature_importances_ / sum(model_o.feature_importances_)) * 100

results = pd.DataFrame({'Features': X_train.columns,
                        'Importances': feature_importances})
results.sort_values(by='Importances', inplace=True)
large = 20; med = 16; small = 12;
params = {'axes.titlesize': large,
          'figure.figsize': (13, 7),
          'axes.labelsize': large,
          'axes.titlesize': large,
          'xtick.labelsize': large,
          'ytick.labelsize': large,
          'figure.titlesize': large}
plt.rcParams.update(params)

plt.figure(figsize=(15,10))
ax = plt.barh(results['Features'], results['Importances'])
plt.xlabel('Importance percentages')
plt.show()

