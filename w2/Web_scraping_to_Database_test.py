# importing modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

# URL for scrapping the data
url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

# get URL html
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# soup.find_all('td') will scrape every element in the url's table as td in HTML is 'table data'
data_iterator = iter(soup.find_all('td'))

# data_iterator is the iterator of the table. This loop will keep repeating till there is data available in the iterator
data = []
while True:
    try:
        country = next(data_iterator).text
        confirmed = int("".join(next(data_iterator).text.split(",")))
        deaths = int("".join(next(data_iterator).text.split(",")))
        continent = next(data_iterator).text
        data.append((country, confirmed, deaths, continent))
# StopIteration exception is raised when there are no more elements left to iterate through
    except StopIteration:
        break

# Convert data to a pandas dataframe
df = pd.DataFrame(data, columns = ["country", "confirmed","deaths","continent"])
print(df)

# Insert the datas from dataframe to covid_data_table in covid_data_db database
password = "0000" #Your postgres password
engine = create_engine(f"postgresql+psycopg2://postgres:{password}@localhost/covid_data_db")
df.to_sql("covid_data_table", engine, if_exists='replace', index = False)