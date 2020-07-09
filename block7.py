#
# block7.py: a matplotlib based module for Practice
# Version 3.9.3 - 03. 07. 2020
#
# Copyright (C) 2020  Duuuda
# Created_by: Чунихин Вадим Андреевич
# contact_email: supermen.tut.103103@gmail.com
# educational_email: 70150235@online.muiv.ru
#
# import modules -------------------------------------------------------------------------------------------------------
from matplotlib import pyplot as plt
from matplotlib.ticker import Formatter
# ----------------------------------------------------------------------------------------------------------------------


# Formatter class
class CustomFormatter(Formatter):
    def __init__(self, confirmed):
        self.confirmed = confirmed

    def __call__(self, y, pos=0):
        return y


# slice data -----------------------------------------------------------------------------------------------------------
def slice_by_countries(func):
    def wrapper(*args, **kwargs):
        all_data = func(*args, **kwargs)
        for country in all_data['Country/Region'].unique():

            yield all_data[all_data['Country/Region'] == country][['Price',
                                                                   'Confirmed',
                                                                   'Deaths',
                                                                   'Recovered',
                                                                   'Recovered/Confirmed %',
                                                                   'Deaths/Confirmed %',
                                                                   'ObservationDate']], country
    return wrapper


@slice_by_countries
def get_data():
    from block6 import RESULT
    return RESULT
# ----------------------------------------------------------------------------------------------------------------------


# plot graphs ----------------------------------------------------------------------------------------------------------
def plot_graph(data, country):
    data = data[['Price',
                 'Confirmed',
                 'Deaths',
                 'Recovered',
                 'Recovered/Confirmed %',
                 'Deaths/Confirmed %']]
    fig = plt.figure(figsize=(15, 10))
    plt.matshow(data.corr(), fignum=fig.number, cmap='inferno')
    ticks = ['BTC Price'] + data.columns.tolist()[1:-2] + ['Recovered÷\nConfirmed %', 'Deaths÷\nConfirmed %']
    plt.xticks(range(data.shape[1]), ticks, fontsize=15)
    plt.yticks(range(data.shape[1]), ticks, fontsize=15)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=20)
    plt.title(f'{country} correlation matrix', fontsize=25, pad=40)
    plt.show()
    # На данных графиках наблюдается некоторая зависимость количества подтвержденных случаев от цены биткоина
    # Для более подробного рассмотрения завистимости построим 2 дополнительных графика


def plot_graph_2(all_data):
    for data_and_country in all_data:
        data, country_name = data_and_country
        formatter = CustomFormatter(data['Confirmed'])
        fig = plt.figure(figsize=(20, 10))
        ax1 = fig.add_subplot(111)
        ax1.yaxis.set_major_formatter(formatter)
        ax1.plot(data['ObservationDate'],
                 data['Confirmed'],
                 '-g',
                 label="Confirmed",
                 lw=2)
        ax1.set_ylabel('Количество заболевших чел.', color='green')
        ax1.legend(loc='upper left')
        ax1.grid(True)
        ax2 = ax1.twinx()
        ax2.yaxis.set_major_formatter(formatter)
        ax2.plot(data['ObservationDate'],
                 data['Price'],
                 '-r',
                 label="BTC_Price",
                 lw=2)
        ax2.set_ylabel('Цена Биткоина $', color='red')
        ax2.legend(loc='upper right')
        ax2.grid(True)
        plt.title(country_name)
        plt.show()
        # После построения данных графиков, действительно видна зависимость двух (на первый взгляд независимых) параметров
        # Из этого можно сделать вывод, что мы имеем дело с ложной корреляцией
# ----------------------------------------------------------------------------------------------------------------------


# main cycle -----------------------------------------------------------------------------------------------------------
def main():
    for country_data in get_data():
        plot_graph(*country_data)
    plot_graph_2(get_data())
# ----------------------------------------------------------------------------------------------------------------------


# start the program ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
