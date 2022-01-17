# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
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
    steak_items = data[data['item_name'].str.contains("Steak")]
    print(steak_items)
    count_steak_items = steak_items.groupby('item_name').agg({'quantity': 'sum'}).quantity.sum()
    steak_group_by_order_id = steak_items.groupby('order_id').agg({'quantity': 'sum'})
    
    print('Всего было заказано стейков:' + str(count_steak_items) )
    print('Среднее количество стейков в заказе: ' + str(round(steak_group_by_order_id['quantity'].mean(), 2)))
    print('Медиана стейков в заказе: ' + str(steak_group_by_order_id['quantity'].median()))
    print('Минимальное количество стейков в заказе: ' + str(steak_group_by_order_id['quantity'].min()))
    print('Максимальное количество стейков в заказе: ' + str(steak_group_by_order_id['quantity'].max()))
    print('Стандартное отклонение количества стейков в заказе: ' + str(round(steak_group_by_order_id['quantity'].std(), 2)))
   
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

    new_data = steak_items
    new_data = new_data[['order_id', 'item_name',
                         'quantity', 'choice_description']]

    hot_sauce = new_data[new_data.choice_description.str.contains('Hot')]
    mild_sauce = new_data[new_data.choice_description.str.contains('Mild')]
    medium_sauce = new_data[new_data.choice_description.str.contains('Medium')]

    # 12. Определить цену по каждой позиции в отдельности.

    data['price/quantity'] = round(data['item_price']/data['quantity'], 2)
    data['price/quantity'] = data['price/quantity'].map(lambda x: [x])
    prices = data.groupby('item_name').agg(
        {'price/quantity': 'sum'})

    prices = prices['price/quantity'].map(lambda x: np.unique(x)).reset_index()

    mix_positions = prices[prices['item_name'].str.contains(
        'and')].copy(deep=True)

    chips_prices = prices[prices['item_name'] == 'Chips']
    prices = prices[~prices.item_name.str.contains("Chips and")]

    mix_positions[['main', 'dependence']] = mix_positions['item_name'].str.split(
        ' and ', 1, expand=True)

    mix_positions['main'], mix_positions['dependence'] = np.where(
        prices.item_name.isin( ["Chips"]).any(), (mix_positions['main'], mix_positions['dependence']), (mix_positions['dependence'], mix_positions['main']))

    mix_positions['price_main'] = mix_positions.main.apply(
        lambda x: prices.loc[prices.item_name == x, 'price/quantity'].values[0])
    mix_positions = mix_positions.explode('price_main')
    mix_positions.sort_values(['main', 'price_main'], ascending=[
                              False, True], inplace=True)
 
    def substructValues(arr, value):
        return [round(x - value, 2) for x in arr]

    mix_positions['price_dependence']  = mix_positions.apply(lambda f: substructValues(f['price/quantity'],f['price_main']), axis=1)
    multi = mix_positions[['main', 'price_main','dependence', 'price_dependence']].set_index(['main', 'price_main', 'dependence'])
    
    print('Цены по каждой позиции: ')
    print(prices)
    print(multi)
    
    