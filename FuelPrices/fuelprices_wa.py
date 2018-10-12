from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import datetime

class FuelPrices_WA:

    def __init__(self):
        self.state = 'WA'

    def main(self):

        fueltypes = ['ULP', 'PULP', 'Diesel', '98 RON', 'E85', 'LPG']
        url = 'https://www.fuelwatch.wa.gov.au/fuelwatch/pages/public/quickSearch.jspx'
        browser = webdriver.Chrome(executable_path='\\\\iml-fs-01\Work Data\\RESEARCH\\Personal Folders\\Jeremy\\WebScraping\\FuelPrices\\chromedriver.exe')
        prices = []
        stations = []
        date = datetime.today().strftime('%Y-%m-%d')

        for fueltype in fueltypes:
            for region in ['All Metro', 'All Country']:

                browser.get(url)
                fueltype_dropdown = browser.find_element_by_xpath("//select[@class = 'iceSelOneMnu']")
                fueltype_dropdown.find_element_by_xpath("//option[contains(text(), '" + fueltype + "')]").click()
                region_dropdown = browser.find_element_by_xpath("//select[@id='quickSearch:region']")
                region_dropdown.find_element_by_xpath("//option[contains(text(), '" + region + "')]").click()
                search_button = browser.find_element_by_xpath("//input[@id='quickSearch:search']")
                time.sleep(1)
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
                    price = items[0].find('span', class_='iceOutTxt').text.strip()
                    brand = items[2].find('span', class_='iceOutTxt').text.strip()
                    name = items[3].find('span', class_='iceOutTxt').text.strip()
                    address = items[4].find('span', class_='iceOutTxt').text.strip()
                    suburb = items[5].find('span', class_='iceOutTxt').text.strip()
                    state = 'WA'
                    postcode = ''
                    id = name + '|' + address
                    prices.append([date, id, fueltype, price])
                    stations.append([id, brand, name, address, suburb, state, postcode])

        browser.quit()

        df_prices = pd.DataFrame(prices, columns=['date', 'id', 'fueltype', 'price'])
        df_prices = df_prices.drop_duplicates(subset=['date', 'id', 'fueltype'])
        df_stations = pd.DataFrame(stations, columns=['id', 'brand', 'name', 'address', 'suburb', 'state', 'postcode'])
        df_stations = df_stations.drop_duplicates()

        # return dictionary of dataframes
        dictData = {'stations': df_stations,
                    'prices': df_prices}

        return dictData

if __name__ == "__main__":
    fp_wa = FuelPrices_WA()
    fp_wa.main()