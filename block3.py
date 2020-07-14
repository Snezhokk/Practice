import pandas as pds
import matplotlib.pyplot as mpl

#   Выполнил Патафеев Владислав
#   построить график по дням с 01.02.2020 по 29.02.2020
#   *количество подтвержденных случаев заражения короновирусом по всему миру
#   *количество случаев выздоровления короновирусом по России (Russia)
df = pds.read_csv("covid_19_data.csv")
#
df['ObservationDate'] = pds.to_datetime(df['ObservationDate'])
df['Day'] = df['ObservationDate'].apply(lambda x: x.day)
# Упрощение даты
data = df.loc[(df['ObservationDate'] >= '02/01/2020') & (df['ObservationDate'] <= '02/29/2020')]


# Отсеивание по дням с 01.02.2020 по 29.02.2020
def filter_russia():
    data_russia = data.loc[(data['Country/Region'] == 'Russia')]
    return data_russia[['Day', 'Recovered']]


def filter_world():
    return data[['Day', 'Confirmed']].groupby(['Day']).sum()


def graphs():
    x = filter_russia()['Day']
    y = filter_world()['Confirmed']
    z = filter_russia()['Recovered']
    mpl.figure(figsize=(13, 6))
    #   Первый график
    mpl.subplot(2, 1, 1)
    mpl.title('Количество случаев заражения короновирусом в мире за февраль', fontsize=14)
    mpl.xlabel("Февраль, день", fontsize=9)
    mpl.ylabel('Количество, тыс.')
    mpl.subplots_adjust(hspace=0.35)
    mpl.plot(x, y, 'r', label='Вылечившихся')
    mpl.legend()
    mpl.grid(which='major', color='k')
    mpl.minorticks_on()
    #   Второй график
    mpl.subplot(2, 1, 2)
    mpl.title('Количество случаев выздоровления короновирусом по России (Russia)', fontsize=14)
    mpl.xlabel("Февраль, день", fontsize=9)
    mpl.ylabel('Количество, чел.')
    mpl.grid(which='major', color='k')
    mpl.plot(x, z, 'g', label='Подтвержденных случаев')
    mpl.legend()
    mpl.minorticks_on()
    mpl.show()


if __name__ == '__main__':
    graphs()
