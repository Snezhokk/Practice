import pandas as pd
from block5 import csv_russia_april_summarized, csv_usa_april_summarized
from datetime import datetime

# BLOCK 6
# Получить Dataset (данные) в формате *.txt и/или *.csv из другого источника
# В качестве источника данных выбрать данные из другой области, например,
# данные метеонаблюде-ний (средняя температура) за такой же период времени.
# Источник данных найти самостоятельно. Данные очистить и объединить, например по полю (столбцу) «Дата».

# Блок выполнил Евгений Малых

# Ссылка на DataSet BitCoin
# https://www.kaggle.com/mehranmazhar/bitcoin-historical-data


def bitcoin_date_filtered():
    # Получение DataFrame из файла
    dataframe = pd.read_csv('Bitcoin_Historical_Data_Daily_2010-07-18_2020-06-25.csv')
    # Фильтрация и возврат по дате 01.04.2020 - 30.04.2020
    filtered = dataframe.loc[(dataframe['Date'] >= '2020-04-01') & (dataframe['Date'] <= '2020-04-30')]
    filtered = filtered.copy()
    # Переименование столбца Date > ObservationDate для сдерживания стандарта
    filtered.rename(columns={'Date': 'ObservationDate'}, inplace=True)
    # Цену в нормальный вид
    filtered['Price'] = filtered['Price'].str.replace(',', '').replace('.', ' ').astype(float)
    # Изменение формата даты из %Y-%m-%d в число дня в месяце
    filtered['ObservationDate'] = list(map(lambda date: datetime.strptime(date, '%Y-%m-%d').day,
                                           filtered['ObservationDate']))
    return filtered[['ObservationDate', 'Price']]


def merge():
    bitcoin = bitcoin_date_filtered()
    # Склеивание фильтрованного датафрейма биткоинов с полученным датафрейма из block5
    usa = csv_usa_april_summarized.merge(bitcoin, on='ObservationDate', how='right')
    russia = csv_russia_april_summarized.merge(bitcoin, on='ObservationDate', how='right')
    return usa.merge(russia, how='outer')


# Переменная с результатом для импорта
RESULT = merge()


if __name__ == '__main__':
    print(RESULT)
