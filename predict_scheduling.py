import numpy as np 
import pandas as pd
import greedy 


def transform_data(data, time_column='dttm'):
    '''
    Transform data to relaible format in order to predict scheduling time 

    Parametrs
    ---------
    data : pd.DataFrame
        DataFrame with time and courier count columns
    time_column : str
        Name of time column in dataframe
    '''
    # Переводит колонку с временем к нужному формату (нужно менять название колонки, если она будет по другому называться)
    data[time_column] = pd.to_datetime(data[time_column], format='%Y-%m-%d %H:%M:%S')
    # Выделим отдельные колонки под дату и время 
    data['date'] = data.time_column.dt.date
    data['hour'] = data.time_column.dt.hour
    
    # Создадим сводную таблицу для более простой работы
    df = pd.pivot(data, index=['delivery_area_id', 'date'], columns='hour', values='partners_cnt').reset_index()

    # Теперь нужно создать колонку в которой будет записан список,
    # в который мы поместим все значения с колонок, в которых находится информация с кол-вом курьеров
    # в определенный день и время 
    cols = [x for x in range(7, 24)]
    df['lists'] = df[cols].to_numpy().tolist()
    # Удалим nan из листов 
    df['lists'] = df['lists'].apply(lambda x: [int(i) for i in x if str(i) != 'nan'])

    return df

def make_scheduling_predict(workloads):
    
    shift_hours = [4, 5, 6, 7, 8]
    need_workload = workloads.copy()
    
    while greedy.is_left_hours(workloads):
        best_shift = 0
        best_pos, best_hour = greedy.get_greed(shift_hours[0], workloads)
        for current_shift, hour in enumerate(shift_hours[1:]):
            current_pos, current_hour = greedy.get_greed(hour, workloads)
            if best_hour < current_hour:
                best_pos = current_pos
                best_hour = current_hour
                best_shift = current_shift + 1 # +1 потому что первый свдиг мы делаем до for
        # Ставим смену
        duration = shift_hours[best_shift]
        for i in range(best_pos, best_pos+duration):
            workloads[i] -= 1
        
    current_workload = [need_workload[i] - workloads[i] for i in range(len(need_workload))]

    return current_workload
    
# Пример вызова функций:
# dateframe = transform_data(data, time_column='dttm') # Преобразует датафрейм к нужному формату
# dateframe['predicted_schedule'] = dateframe['lists'].apply(lambda x: make_scheduling_predict(x)) # Итерируется по каждому списку и делает 
                                                                                                   # заполнение смен через жадный алгоритм



