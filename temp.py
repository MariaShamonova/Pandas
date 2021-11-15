# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean


def getPositionInOrder(data, columns):
    data_temp = data[columns]
    position_in_order = data_temp.groupby(
        list(data_temp)).size().reset_index(name="count")
    position_in_order['count'] = position_in_order['quantity'].mul(
        position_in_order['count'])
    position_in_order = position_in_order.drop('quantity', 1)

    return position_in_order


if __name__ == "__main__":
    data = pd.read_csv(
        'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv', sep='\t')
    pd.options.display.max_columns = None
    pd.options.display.max_colwidth = None
    temp = data['choice_description'].head(20)

    number_observerations = len(data.index)
    all_columns = data.columns
    most_common_values = data['item_name'].mode().values

    print("Number of observations: ", number_observerations)
    print('Columns: ', ', '.join(list(data.columns)))
    print("Most common values: ",  ', '.join(most_common_values))

    data_frequency = data['item_name'].value_counts()
    data_frequency.plot(kind='bar', figsize=(95, 30), fontsize=100)

    col = 'item_price'
    old_type_column = data[col].dtypes
    data[col] = data[col].apply(lambda x: float(
        x.replace('$', '').replace(' ', '')))
    new_type_column = data[col].dtypes
    print("Change type of column 'item_price' from ",
          old_type_column, " to ", new_type_column)

    agg_func_math = {
        'item_price': ['sum']
    }

    # 5
    series_group_by_price = data.groupby(['item_name']).agg(agg_func_math)
    enam_index = list(range(1, len(series_group_by_price) + 1))
    series_group_by_price['index'] = enam_index

    x = series_group_by_price['index'].values
    y = list(series_group_by_price['item_price']['sum'].round(2))

    plt.bar(x, y)

    # Средняя сумма заказа( 3 способа )

    # Способ 1
    agg_func_math = {
        'item_price': ['sum']
    }
    orders = data.groupby(['order_id']).agg(agg_func_math)
    mean_value = orders.mean(0)

    print("Средняя сумма заказа (способ № 1): ", mean_value)

    # Способ 2
    list_orders = list(orders['item_price']['sum'])
    mean_value = sum(list_orders) / len(list_orders)
    print("Средняя сумма заказа (способ № 2): ", mean_value)

    # Способ 3
    mean_list = mean(list_orders)
    print("Средняя сумма заказа (способ № 3): ", mean_value)

    # Среднее, максимальное и медианное значение позиций в заказе
    count_position = data.groupby(['order_id']).agg({'item_name': ['count']})
    list_count_position = count_position['item_name']['count']

    mean_value = round(mean(list(list_count_position)), 4)
    print('Среднее значение позиций в заказе: ', mean_value)

    max_value = list_count_position.max()
    print('Максимальное значение позиций в заказе: ', max_value)

    median_value = list_count_position.median()
    print('Медианное значение позиций в заказе: ', median_value)

    # 9.  Определить статистику заказов стейков, а также статистику заказов прожарки.

    #new_data = data[data['A'].str.contains("hello")]

    # 10. Добавить новый столбец цен на каждую позицию в заказе в рублях.
    # print(data)
    print('Введите текущий курс доллара: ')
    dollar = float(input().replace(',', '.'))
    data['item_price_rub'] = data['item_price'].map(lambda x: x * dollar)

    # 11. Сгруппировать заказы по входящим позициям в него.
    # Отдельно сгруппировать по стейкам во всех видах прожарках.

    data_temp = data[['order_id', 'item_name', 'quantity']]
    columns = ['order_id', 'item_name', 'quantity']
    position_in_order = getPositionInOrder(data_temp, columns)
        
    print("Заказы по входящим позициям в него: ")
    print(position_in_order)

    new_data = data[data['item_name'].str.contains("Steak")]
    new_data = new_data[['order_id', 'item_name',
                         'quantity', 'choice_description']]

    new_data['sauce'] = new_data['choice_description'].map(
        lambda x: (('Hot: ' + str(x.count("Hot")) + ' ') if '(Hot)' in x else '') +
        (('Medium: ' + str(x.count("Medium")) + ' ') if 'Medium' in x else '') +
        (('Melt: ' + str(x.count("Melt"))) if '(Melt)' in x else '')
    )

    def getUniqueValue(arr):
        return 'Hot' in arr or 'Melt' in arr or 'Medium' in arr

    new_data['choice_description'] = new_data['choice_description'].map(
        lambda x: list(filter(getUniqueValue, x.replace('[', '').replace(']', '').split(','))))
    new_data.drop(new_data[new_data['choice_description'].str.len() == 0 ].index, inplace = True)
  
    print(new_data.head(20))

