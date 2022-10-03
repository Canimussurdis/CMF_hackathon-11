def get_greed(shift_hour, workload):
    #  "Форточка" в shift_hour часов
    start_pos = 0
    end_pos = shift_hour - 1

    best_pos = 0
    best_hour = sum(workload[start_pos:end_pos + 1])
    start_pos += 1
    end_pos += 1
    while end_pos < len(workload):
        current_hour = sum(workload[start_pos:end_pos + 1])
        if best_hour < current_hour:
            best_pos =  start_pos
            best_hour = current_hour
        start_pos += 1
        end_pos += 1
    return best_pos, best_hour


def is_left_hours(workload):
    for hour in workload:
        if hour > 0:
            return True
    return False


shift_hours = [4, 5, 6, 7, 8]
shift_hours.sort() # Опционально, если список изначально не сортирован
workload = [1, 5, 3, 1, 2, 1, 3, 5, 6, 3, 1]
while is_left_hours(workload):
    best_shift = 0
    best_pos, best_hour = get_greed(shift_hours[0], workload)
    for current_shift, hour in enumerate(shift_hours[1:]):
        current_pos, current_hour = get_greed(hour, workload)
        if best_hour < current_hour:
            best_pos = current_pos
            best_hour = current_hour
            best_shift = current_shift + 1 # +1 потому что первый свдиг мы делаем до for
    # Ставим смену
    duration = shift_hours[best_shift]
    for i in range(best_pos, best_pos+duration):
        workload[i] -= 1
    print(*workload)
    print(f"Была поставлена смена на {duration} часов с {best_pos} по {best_pos+duration-1} часов")
print(f"Количество лишних часов: {-sum(workload)}")


