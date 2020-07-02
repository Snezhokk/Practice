import csv
from datetime import datetime
# 0 - SNo
# 1 - ObservationDate
# 2 - Province/State
# 3 - Country/Region
# 4 - Last Update
# 5 - Confirmed
# 6 - Deaths
# 7 - Recovered


def au_death_cases():
    death_count = 0
    cm_date = datetime(2020, 2, 2)
    with open('covid_19_data.csv', 'r', encoding='UTF8') as csvfile:
        coronareader = csv.reader(csvfile, delimiter=',')
        next(coronareader)  # Пропустить первую строчку с обозначениями
        for row in coronareader:
            ob_date = datetime.strptime(row[1], r'%m/%d/%Y')
            if (cm_date > ob_date):
                if (row[3] == 'Australia'):
                    death_count += int(float(row[6]))  # string - float - int
            else:
                break  # Если список отсортирован, как в этом случае
    return death_count  # 0


def confirmed_cases():
    confirmed_count = 0
    cm_date = datetime(2020, 2, 2)
    with open('covid_19_data.csv', 'r', encoding='UTF8') as csvfile:
        coronareader = csv.reader(csvfile, delimiter=',')
        next(coronareader)
        for row in coronareader:
            ob_date = datetime.strptime(row[1], r'%m/%d/%Y')
            if (cm_date > ob_date):
                confirmed_count += int(float(row[5]))
            else:
                break
    return confirmed_count  # 50573
