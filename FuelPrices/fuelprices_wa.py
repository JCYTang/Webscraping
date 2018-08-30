from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import os
from datetime import datetime

fueltypes = ['ULP', 'PULP', 'Diesel', '98 RON', 'E85']
url = 'https://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/quickSearch.jspx'
browser = webdriver.Chrome()
prices = []
stations = []
date = datetime.today().strftime('%Y-%m-%d')

for fueltype in fueltypes:

    browser.get(url)
    fueltype_dropdown = browser.find_element_by_xpath("//select[@class = 'iceSelOneMnu']")
    fueltype_dropdown.find_element_by_xpath("//option[contains(text(), '" + fueltype + "')]").click()
    search_button = browser.find_element_by_xpath("//input[@id='quickSearch:search']")
    search_button.click()
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'iceDatTblCol')))
    items_per_page_button = browser.find_element_by_xpath("//select[@class = 'iceSelOneMnu']")
    items_per_page_button.find_element_by_xpath("//option[@value = '99999']").click()
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all(class_=re.compile('iceDatTblRow.*'))
    for row in rows:
        items = row.find_all('td', class_='iceDatTblCol')
        price = items[0].find('span', class_='iceOutTxt').text
        brand = items[2].find('span', class_='iceOutTxt').text
        name = items[3].find('span', class_='iceOutTxt').text
        address = items[4].find('span', class_='iceOutTxt').text
        suburb = items[5].find('span', class_='iceOutTxt').text
        state = 'WA'
        id = name + '|' + address
        prices.append([date, id, fueltype, price])
        stations.append([id, brand, name, address, suburb, state])

browser.quit()

df_prices = pd.DataFrame(prices, columns=['date', 'id', 'fueltype', 'price'])
df_stations = pd.DataFrame(stations, columns=['id', 'brand', 'name', 'address', 'suburb', 'state'])
df_stations = df_stations.drop_duplicates()

archive_folder = 'W:\RESEARCH\Personal Folders\Jeremy\WebScraping\FuelPrices\Archive'
df_stations.to_csv(os.path.join(archive_folder, 'fuelstations_wa.csv'), index=False)
df_prices.to_csv(os.path.join(archive_folder, 'fuelprices_wa_' + datetime.today().strftime('%Y%m%d') + '.csv'), \
    index=False)