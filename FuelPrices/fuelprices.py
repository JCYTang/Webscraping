from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from string import ascii_lowercase
import itertools
import re
import time
import csv
import pandas as pd

#consider using a crawler to hit all the locations
#loop through the relevant petrol types E10, 91, 95, 98, Diesel, Premium Diesel
#otherwise use a list of valid postcodes and suburbs and change the url, or loop through 2 letter combos
#send keys to search form
#loop through all available results
#submit into search form and run request
#use a timeout and headers on browser.get
#use header to stop site from knowing it is being hit by a web scraper
#test response code
#work out how to test when pages are loaded, otherwise send sleep commands

def scrape_location(browser, location):

    #scrape petrol prices for a given location
    isDropDownItemSelectable = False
    while not isDropDownItemSelectable:
        search_form = browser.find_element_by_id('txtbxSuburbPostCode')
        search_form.clear()
        search_form.send_keys(location)
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element_value((By.ID, 'txtbxSuburbPostCode'), location))
        try:
            drop_down = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'dropdown-menu')))
        except TimeoutException:
            drop_down = browser.find_element_by_class_name('dropdown-menu')
        try:
            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//li'))).click()
            isDropDownItemSelectable = True
        except TimeoutException:
            search_form.clear()
    search_button = browser.find_element_by_xpath("//button[@class = 'button expand nextpage search-button']")
    #time.sleep(1.2)
    search_button.click()
    isPageLoaded = False
    while not isPageLoaded:
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'result-item')))
            isPageLoaded = True
        except TimeoutException:
            browser.refresh()

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    stations = soup.find_all('p', class_='result-item')
    for station in stations:
        # only scrape if price is a float
        price = station.find('span', class_='price').text
        if price != 'n/a':
            price = float(price)
            name = station.find('span', class_='station').b.text
            address = station.find('span', class_='tiny').text
            # suburb = address[address.find(',') + 1:address.find('NSW')].strip()
            # brand = station.find('span', class_='caltex-logo').img['src']
            # name = re.sub(suburb, '', name, flags=re.IGNORECASE).strip()
            names.append(name)
            fueltypes.append(fueltype)
            addresses.append(address)
            prices.append(price)
            print('name:\t' + name, 'type:\t' + fueltype, 'address:\t' + address, 'price:\t' + str(price))
            with open('fuel_prices.csv', 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([name, fueltype, address, price])

    browser.back()

url = 'https://www.fuelcheck.nsw.gov.au/app'
browser = webdriver.Chrome()
browser.get(url)
keywords = [''.join(i) for i in itertools.product(ascii_lowercase, repeat = 2)]
prices = []
names = []
addresses = []
fueltypes = ['E10', 'U91', 'P95', 'P98', 'DL', 'PDL']
filename = 'fuel_prices.csv'

#loop through and set fuel types
fueltype = 'E10'

#loop through all combinations of 2 letter words
for keyword in keywords:
    search_form = browser.find_element_by_id('txtbxSuburbPostCode')
    search_form.clear()
    search_form.send_keys(keyword)
    try:
        drop_down = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dropdown-menu')))
    except TimeoutException:
        drop_down = browser.find_element_by_class_name('dropdown-menu')

    locations = drop_down.text
    if locations != '':
        for location in locations.splitlines():
            scrape_location(browser, location)

browser.quit()


# df_prices = pd.DataFrame({'brand': names,
#                           'fueltype': fueltypes,
#                           'price': prices,
#                           'address': addresses})
# df = df_prices.drop_duplicates()
# df_prices.to_csv('fuel_prices.csv')


#loop through all postcodes, append requests

#get suburb from address, words after comma but before NSW
#remove suburb from brand name to get the brand


