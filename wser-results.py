import requests
import datetime
from bs4 import BeautifulSoup
import csv
import os


def get_column(column):
    data = []
    cells = table.find_all("td", class_=column)
    for cell in cells:
        data.append(cell.text)
    return data


# 1975 had one starter and no finishers. 2008 was cancelled
# due to numerous wildfires. 2020 was cancelled due to COVID-19.
NO_RESULT_RACES = [1975, 2008, 2020]
race_year = 1974  # The first WSER was in 1974.


# output directory path
path = './wser-results'
# create directory if it does not exist
if not os.path.exists(path):
    os.mkdir(path)

# The WSER is the last weekend of June. Assume WSER results
# for the current year have been posted by July 1st.
WSER_results_posted = datetime.datetime(datetime.datetime.now().year, 7, 1)
if datetime.datetime.now() >= WSER_results_posted:
    most_recent_race_year = datetime.datetime.now().year
else:
    most_recent_race_year = datetime.datetime.now().year - 1

# Loops through every race year
while most_recent_race_year >= race_year:
    page = requests.get("https://www.wser.org/results/% s-results/"
                        % race_year)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table')
    headers = table.find_all('th')
    header_list = []
    for header in headers:
        header_list.append(header.text)
    place, time, bib, first, last = [], [], [], [], []
    gender, age, city, state_country = [], [], [], []
    place = get_column("column-1")  # Place is always column-1
    time = get_column("column-2")  # Time is always column-2
    if race_year >= 2003:
        bib = get_column("column-3")
        first = get_column("column-4")
        last = get_column("column-5")
        gender = get_column("column-6")
        age = get_column("column-7")
        city = get_column("column-8")
        state_country = get_column("column-9")
        columns = ["Place", "Time", "Bib", "First", "Last", "Gender", "Age",
                   "City", "State/country"]
        # Changes columns to rows
        rows = zip(place, time, bib, first, last, gender,
                   age, city, state_country)
    else:
        first = get_column("column-3")
        last = get_column("column-4")
        gender = get_column("column-5")
        age = get_column("column-6")
        columns = ["Place", "Time", "First", "Last", "Gender", "Age"]
        # Changes columns to rows
        rows = zip(place, time, first, last, gender, age)
    # Writes race results for current race year to CSV
    with open("wser-results/WSER_% s.csv" %
              race_year, "w") as f:
        write = csv.writer(f)
        write.writerow(columns)
        write.writerows(rows)
    race_year += 1
    if race_year in NO_RESULT_RACES:  # Skip race result pages with no results
        race_year += 1
