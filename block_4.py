import os
import pandas as pd


def get_dataset(filename):
    # Сделать очистку данных
    reader = pd.read_csv(filename, sep=',')
    dataset = pd.DataFrame(reader)

    return dataset


def calculate_deaths_per_confirmed(dataset):
    dataset['deaths/confirmed rate'] = dataset.apply(
        lambda row: row.Deaths / row.Confirmed if row.Confirmed > 0 and row.Deaths > 0 else 0, axis=1)


def calculate_recovered_per_confirmed(dataset):
    dataset['recovered/confirmed rate'] = dataset.apply(
        lambda row: row.Recovered / row.Confirmed if row.Confirmed > 0 and row.Recovered > 0 else 0, axis=1)


def main():
    dataset = get_dataset('covid_19_data.csv')
    calculate_deaths_per_confirmed(dataset)
    calculate_recovered_per_confirmed(dataset)

    print(dataset)
