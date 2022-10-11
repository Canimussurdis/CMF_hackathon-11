# Прогноз спроса и планирование рабочих смен

### Команда 11
---
**Цель**: создать продукт (код), который на ежедневной основе "тригерит" фунцию (F) для подсчета рабочих смен.  

**Задачи**:
- Спрогнозировать количество заказов по часам на 7 дней вперед
- В зависимости от того, сколько будет в i-й час заказов, рассчитать, сколько надо курьеров
- Потребность в курьерах разбить на смены (от 4-х до 8-ми сменами)
---
## Алгоритм решения
- Проведена кластеризация временных рядов
- Получение признаков для дальнейшего анализа (в том числе праздников)
- Предсказание опоздания для каждой отдельной площадки
- На основное полученного результата получены рабочие часы для различных зон доставки (schedule.csv)
- Подсчет требуемого количества курьеров
- Реализация жадного алгоритма для расчета смен 
---
### Задача 1: Прогноз числа заказов по часам


### Задача 2: Определение числа курьеров
  Для каждой площадки используется классификатор (логистическая регрессия), который определяет по заданным значениям числа заказов и числа курьеров, будет ли delay_rate иметь допустимое значение (delay_rate < 0.05) (класс 0) или нет (класс 1). Число курьеров определяется путём подбора числа курьеров от 1 до тех пор пока классификатор не выдаст 0 при данном числе заказов. Повторяя данную процедуру для каждого часа, получаем требуемое числа курьеров в различные моменты времени.
  
### Задача 3: Cоставление расписания смен курьеров 
Для составления расписания использовался алгоритм "жадного перебора". Работает по схеме "шторки" или "форточки": ищем по запросу (список часов) максимальное количество часов, которое может брать смена за 4,5,6,7,8 часов, и просто ставим эту смену. 

Идем от меньшей смены до большей. 

Как находим лучшую смену для определенной ситуации - убираем часы и считаем дальше. 
