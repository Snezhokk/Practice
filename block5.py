

# <блок Тюменева Владислава Дмитриевича>
import pandas
import matplotlib.pyplot as plt

import math
import datetime

csv = pandas.read_csv('covid_19_data.csv')

csv_russia = csv.loc[csv['Country/Region'] == 'Russia']
csv_usa = csv.loc[csv['Country/Region'] == 'US']

csv_russia_april = csv_russia.loc[
    (csv_russia['ObservationDate'] >= '04/01/2020') & (csv_russia['ObservationDate'] <= '04/30/2020')
]

csv_usa_april = csv_usa.loc[
    (csv_usa['ObservationDate'] >= '04/01/2020') & (csv_usa['ObservationDate'] <= '04/30/2020')
]

russia_population = 146748590
usa_population = 329210630


def summarize_data_by_date(dataframe):
    summarized_dict = {
        'ObservationDate': [],
        'Confirmed': [],
        'Deaths': [],
        'Recovered': [],
    }

    country_name = dataframe.iloc[0]['Country/Region']

    population = russia_population if country_name == "Russia" else usa_population

    for index, row in dataframe.iterrows():
        # datetime -> day number
        date = datetime.datetime.strptime(row['ObservationDate'], '%m/%d/%Y').day

        try:
            recovered_index = summarized_dict['ObservationDate'].index(date)
        except ValueError:
            summarized_dict['ObservationDate'].append(date)

            for key in ['Confirmed', 'Deaths', 'Recovered']:
                summarized_dict[key].append(0)

            recovered_index = len(summarized_dict['ObservationDate']) - 1

        for key in ['Confirmed', 'Deaths', 'Recovered']:
            summarized_dict[key][recovered_index] += int(row[key])

    summarized_dict['Country/Region'] = [country_name] * len(summarized_dict['ObservationDate'])

    df = pandas.DataFrame(summarized_dict)

    df["Recovered/Confirmed %"] = df.apply(lambda row: (row["Recovered"]/row["Confirmed"]) * 100, axis=1)
    df["Deaths/Confirmed %"] = df.apply(lambda row: (row["Deaths"] / row["Confirmed"]) * 100, axis=1)

    df.loc[0, 'dynamic(Recovered/Confirmed %)/population'] = (df.loc[0, 'Recovered'] / df.loc[0, 'Confirmed']) * 100 / population
    df.loc[0, 'dynamic(Deaths/Confirmed %)/population'] = (df.loc[0, 'Deaths'] / df.loc[
        0, 'Confirmed']) * 100 / population

    for i in range(1, len(df)):
        df.loc[i, 'dynamic(Recovered/Confirmed %)/population'] = (df.loc[i, 'Recovered'] / df.loc[i, 'Confirmed']) * 100 / population - df.loc[i - 1, 'dynamic(Recovered/Confirmed %)/population']
        df.loc[i, 'dynamic(Deaths/Confirmed %)/population'] = (df.loc[i, 'Deaths'] / df.loc[
            i, 'Confirmed']) * 100 / population - df.loc[i - 1, 'dynamic(Deaths/Confirmed %)/population']

    return df


def get_ticks_by_series(series_1, series_2, tick_step=1):
    tick_1_min = series_1.min()
    tick_2_min = series_2.min()
    tick_min = min([tick_1_min, tick_2_min])

    tick_1_max = series_1.max()
    tick_2_max = series_2.max()
    tick_max = max([tick_1_max, tick_2_max])

    tick_first = max([tick_step, math.floor(tick_min / tick_step) * tick_step])
    tick_last = math.ceil(tick_max / tick_step) * tick_step
    ticks = sorted(
        [tick_min] +
        list(range(tick_first, tick_last, tick_step))
    )

    if tick_max not in ticks:
        ticks.append(tick_max)

    return ticks

csv_russia_april_summarized = summarize_data_by_date(csv_russia_april)
csv_usa_april_summarized = summarize_data_by_date(csv_usa_april)

if __name__ == "__main__":
    x_ticks = get_ticks_by_series(csv_russia_april_summarized['ObservationDate'], csv_usa_april_summarized['ObservationDate'], 3)

    # 5.1
    # Смертельные исходы/Заражённые

    y_ticks = get_ticks_by_series(csv_russia_april_summarized['Deaths/Confirmed %'], csv_usa_april_summarized['Deaths/Confirmed %'])

    figure1 = plt.figure("График смертей от коронавируса")
    plt.xlabel('Дата (апрель 2020 года)')
    plt.ylabel('% смертей относительно заболевших')
    plt.yticks(ticks=y_ticks)
    plt.xticks(ticks=x_ticks)
    plt.plot(csv_russia_april_summarized['ObservationDate'], csv_russia_april_summarized['Deaths/Confirmed %'], color='green', label='Россия', markevery=[0, -1])
    plt.plot(csv_usa_april_summarized['ObservationDate'], csv_usa_april_summarized['Deaths/Confirmed %'], color='blue', label='США', markevery=[0, -1])

    plt.grid(axis='x', color='0.95')
    plt.legend(title='Страны:')
    plt.title('График смертей от коронавируса')

    # 5.2
    # Выздоровевшие/Заражённые

    y_ticks = get_ticks_by_series(csv_russia_april_summarized['Recovered/Confirmed %'], csv_usa_april_summarized['Recovered/Confirmed %'])

    figure2 = plt.figure("График выздоровления от коронавируса")
    plt.xlabel('Дата (апрель 2020 года)')
    plt.ylabel('% выздоровевших относительно заболевших')
    plt.yticks(ticks=y_ticks)
    plt.xticks(ticks=x_ticks)
    plt.plot(csv_russia_april_summarized['ObservationDate'], csv_russia_april_summarized['Recovered/Confirmed %'], color='green', label='Россия', markevery=[0, -1])
    plt.plot(csv_usa_april_summarized['ObservationDate'], csv_usa_april_summarized['Recovered/Confirmed %'], color='blue', label='США', markevery=[0, -1])

    plt.grid(axis='x', color='0.95')
    plt.legend(title='Страны:')
    plt.title('График выздоровления от коронавируса')

    # 5.3
    # 5.1 / население
    # 5.2 / население

    y_ticks = get_ticks_by_series(csv_russia_april_summarized['dynamic(Recovered/Confirmed %)/population'], csv_usa_april_summarized['dynamic(Recovered/Confirmed %)/population'])

    figure3 = plt.figure("Динамика выздоровления от коронавируса в зависимости от населения")
    plt.xlabel('Дата (апрель 2020 года)')
    plt.ylabel('динамика % выздоровевших относительно заболевших относительно населения')
    plt.yticks(ticks=y_ticks)
    plt.xticks(ticks=x_ticks)
    plt.plot(csv_russia_april_summarized['ObservationDate'], csv_russia_april_summarized['dynamic(Recovered/Confirmed %)/population'], color='green', label='Россия', markevery=[0, -1])
    plt.plot(csv_usa_april_summarized['ObservationDate'], csv_usa_april_summarized['dynamic(Recovered/Confirmed %)/population'], color='blue', label='США', markevery=[0, -1])

    plt.grid(axis='x', color='0.95')
    plt.legend(title='Страны:')
    plt.title('Динамика выздоровления от коронавируса в зависимости от населения')

    y_ticks = get_ticks_by_series(csv_russia_april_summarized['dynamic(Deaths/Confirmed %)/population'],
                                  csv_usa_april_summarized['dynamic(Deaths/Confirmed %)/population'])
    figure4 = plt.figure("Динамика смертей от коронавируса в зависимости от населения")
    plt.xlabel('Дата (апрель 2020 года)')
    plt.ylabel('динамика % смертей относительно заболевших относительно всего населения')
    plt.yticks(ticks=y_ticks)
    plt.xticks(ticks=x_ticks)
    plt.plot(csv_russia_april_summarized['ObservationDate'], csv_russia_april_summarized['dynamic(Deaths/Confirmed %)/population'], color='green', label='Россия', markevery=[0, -1])
    plt.plot(csv_usa_april_summarized['ObservationDate'], csv_usa_april_summarized['dynamic(Deaths/Confirmed %)/population'], color='blue', label='США', markevery=[0, -1])

    plt.grid(axis='x', color='0.95')
    plt.legend(title='Страны:')
    plt.title('Динамика смертей от коронавируса в зависимости от населения')

    plt.show()

# </блок Тюменева Владислава Дмитриевича>
