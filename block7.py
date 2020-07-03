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
# ----------------------------------------------------------------------------------------------------------------------


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
                                                                   'Deaths/Confirmed %']], country
    return wrapper


@slice_by_countries
def get_data():
    from block6 import RESULT
    return RESULT
# ----------------------------------------------------------------------------------------------------------------------


# plot graphs ----------------------------------------------------------------------------------------------------------
def plot_graph(data, country):
    fig = plt.figure(figsize=(15, 10))
    plt.matshow(data.corr(), fignum=fig.number, cmap='inferno')
    ticks = ['BTC Price'] + data.columns.tolist()[1:-2] + ['Recovered÷\nConfirmed %', 'Deaths÷\nConfirmed %']
    plt.xticks(range(data.shape[1]), ticks, fontsize=15)
    plt.yticks(range(data.shape[1]), ticks, fontsize=15)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=20)
    plt.title(f'{country} correlation matrix', fontsize=25, pad=40)
    plt.show()
# ----------------------------------------------------------------------------------------------------------------------


# main cycle -----------------------------------------------------------------------------------------------------------
def main():
    for country_data in get_data():
        plot_graph(*country_data)
# ----------------------------------------------------------------------------------------------------------------------


# start the program ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------------------------------------------------------
