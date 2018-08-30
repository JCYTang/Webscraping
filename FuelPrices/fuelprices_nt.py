from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import time

fueltypes = ['DL', 'U91', 'P95', 'E10', 'P98', 'PD', 'E85']
regions = [str(i) for i in range(1, 10)]

browser = webdriver.Chrome()

for fueltype in fueltypes:
    for region in regions:
        url = 'https://myfuelnt.nt.gov.au/Home/Results?searchOptions=region&Suburb=&SuburbId=0&RegionId=' + region + \
            '&FuelCode=' + fueltype + '&BrandIdentifier='

        browser.get(url)
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.ID, 'scroll')))
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all(id=re.compile('row.*'))
        for row in rows:
            price = row.find(class_='fuelPrice').strong.text
            try:
                price = float(price)
                brand = row.find('td').find().attrs['src']
                name = row.find(class_='outletdetails').strong.text
                items = [i for i in row.find(class_='outletdetails')]
                address = str(items[-1])
                state = 'NT'
                print(price, fueltype, brand, name, address, state, sep=';')
            except:
                pass


browser.quit()
