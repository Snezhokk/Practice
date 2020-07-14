import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# Блок создал Воровченко Леонид Сергеевич


response = requests.get('https://pogoda1.ru/los-andzheles/april-2020/')
soup = bs(response.content, 'html.parser')
dates = []
pressures = []
humudities = []

for row in soup.find_all('div', {'class': 'calendar-row'}):
    for cell in row.find_all('a', {'class': 'calendar-item'}):
        try:
            link = 'https://pogoda1.ru/' + cell['href']
            req = requests.get(link).content
            data = bs(req, 'html.parser')
            date = cell['href'].split('/')[-2]
            values = data.find_all('span', {'class': 'value'})[:2]
            dates.append(date)
            pressures.append(values[0].text)
            humudities.append(values[1].text)
        except Exception as e:
            pass

d = {'Дата': dates, 'Давление': pressures, 'Влажность': humudities}
df = pd.DataFrame(d)
print(df.to_string())
