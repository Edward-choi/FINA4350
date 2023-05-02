"""
This script fetches Mad Money's stock calls from TheStreet.com's website
with the help of Playwright and BeautifulSoup, and saves the data to /data/thestreet/.
"""
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv
from datetime import date, timedelta
from os.path import join

# output path
output_path = "../data/thestreet/"

# Specify whether to inverse Cramer's calls and date range
inverse = True
start = "2017-01-01"
end = "2021-12-31"

# Specify whether to include Lightning Round's calls
lightning = False

start_date = date(*list(map(int, start.split("-"))))
end_date = date(*list(map(int, end.split("-"))))
delta = timedelta(days=1)

url = "https://madmoney.thestreet.com/screener/index.cfm?showview=stocks&showrows={NUMDATA}&airdate=".format(NUMDATA=1000)
companies = []
symbols = []
dates = []
segments = []
calls = []
prices = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    while start_date <= end_date:
        curr_date = start_date.strftime("%Y-%m-%d")
        start_date += delta
        page.goto(url + curr_date)
        time.sleep(0.5)

        print("Fetching data for {}".format(curr_date))

        soup = BeautifulSoup(page.content(), "lxml")
        table = soup.find("table", {"id": "stockTable"})
        print(table)
        rows = table.find_all("tr")[1:]

        # Checks if table is empty
        if (len(rows) > 1 and rows[1].find("td").find('em') != None):
            print("No data for {}".format(curr_date))
            continue

        # If table not empty, iterate through rows in the table
        else:
            for row in rows:
                tds = row.find_all("td")
                # Skip this row if call was made from lightning round segment (for no_lightning dataset)
                if (not lightning and tds[2].find('img')['alt'] == "L"):
                    continue
                companies.append(tds[0].text)
                symbols.append(tds[0].find('a').text)
                segments.append(tds[2].find('img')['alt'])
                dates.append(curr_date)
                if (inverse):
                    calls.append(6 - int(tds[3].find('img')['alt']))
                else:
                    calls.append(tds[3].find('img')['alt'])
                prices.append(tds[4].text)

    data = zip(companies, symbols, dates, segments, calls, prices)

    if lightning and inverse:
        file_name = 'MadMoneyInversedData_{}_{}.csv'
    elif lightning and not inverse:
        file_name = 'MadMoneyData_{}_{}.csv'
    elif not lightning and inverse:
        file_name = 'MadMoneyInversedData_no_lightning_{}_{}.csv'
    else:
        file_name = 'MadMoneyData_no_lightning_{}_{}.csv'
    file_name = join(output_path, file_name)

    # Save data collected to csv file
    with open(file_name.format(start, end), 'w') as csvfile:
        csv_out = csv.writer(csvfile, lineterminator='\n')
        csv_out.writerow(['Company', 'Symbol', 'Date', 'Segment', 'Call', 'Price'])
        csv_out.writerows(data)

    browser.close()
