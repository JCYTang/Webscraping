import json
import requests
import pandas as pd
import os
from datetime import datetime

def main():

    url = 'https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken'
    headers = {'authorization': 'Basic NWx2aGdqSDVYS05YdkhzT2VSc1Z0d2R0UTNsb0VtTGk6cm5lRHBLS3hHVzY2anpzQg==',}
    params = (('grant_type', 'client_credentials'),)
    response = requests.get(url, params=params, headers=headers)
    access_token = json.loads(response.content)['access_token']

    # set apikey, transactionid, requesttimestamp variables
    apikey = '5lvhgjH5XKNXvHsOeRsVtwdtQ3loEmLi'
    date_format = '%d/%m/%y %I:%M:%S %p'
    requesttimestamp = datetime.today().strftime(date_format)
    headers = {
        'apikey': apikey,
        'transactionid': '1',
        'requesttimestamp': requesttimestamp,
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + access_token,
        }

    url = 'https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices'
    response = requests.get(url, headers=headers)
    data = response.json()

    # get dataframe of stations ready for import
    df_stations = pd.DataFrame(data['stations'])
    df_stations = df_stations[df_stations.columns[[2,1,4,0]]]
    df_stations['suburb'] = df_stations['address'].apply(lambda x: x[x.rfind(',')+1:x.rfind('NSW')].strip().title())
    df_stations['state'] = 'NSW'
    df_stations['postcode'] = df_stations['address'].apply(lambda x: x[-4:])
    df_stations['address'] = df_stations['address'].apply(lambda x: x[:x.rfind(',')])
    df_stations.columns.values[0] = 'id'

    # get dataframe of prices ready for import
    df_prices = pd.DataFrame(data['prices'])
    df_prices = df_prices[df_prices.columns[[1,3,0,2]]]
    df_prices['lastupdated'] = df_prices['lastupdated'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S'))
    df_prices['lastupdated'] = df_prices['lastupdated'].dt.strftime('%Y-%m-%d')
    df_prices.columns.values[0] = 'date'
    df_prices.columns.values[1] = 'id'
    df_prices['price'] = pd.to_numeric(df_prices['price'])

    # save data as csv file
    archive_folder = 'W:\RESEARCH\Personal Folders\Jeremy\WebScraping\FuelPrices\Archive'
    df_stations.to_csv(os.path.join(archive_folder, 'fuelstations_nsw.csv'), index=False)
    df_prices.to_csv(os.path.join(archive_folder, 'fuelprices_nsw_' + datetime.today().strftime('%Y%m%d') + '.csv'), \
        index = False)


if __name__ == "__main__":
    main()