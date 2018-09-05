from datetime import datetime
from fuelprices_nsw import FuelPrices_NSW
from fuelprices_wa import FuelPrices_WA
from fuelprices_qldvic import FuelPrices_QLDVIC
import pandas as pd
import os

class WebScraping():
    '''initialize with a script class'''

    def __init__(self, script):
        self.data = {}
        self.script = script
        self.files = []
        self.archive_folder = 'W:\\RESEARCH\\Personal Folders\\Jeremy\\WebScraping\\FuelPrices\\Archive'

    def save_to_csv(self):
        '''save dictionary of dataframes as csv files'''

        datestamp = datetime.today().strftime('%Y%m%d')
        stations_file = os.path.join(self.archive_folder, 'fuelstations_' + self.script.state + '.csv')
        prices_file = os.path.join(self.archive_folder, 'fuelprices_' + self.script.state + '_' + datestamp + '.csv')
        self.data['stations'].to_csv(stations_file, index=False)
        self.data['prices'].to_csv(prices_file, index=False)
        self.files.append(stations_file)
        self.files.append(prices_file)

    def insert_to_database(self, files):
        ''''upload csv files to database'''

    def execute_script(self):
        '''execute script and return a dictionary of dataframes'''

        self.data = self.script.main()

    def standardize_names(self, map_file, field):
        '''standardize brand and fueltype names'''

        df_map = pd.read_excel(map_file, sheet_name=field)
        if field == 'brand':
            df = self.data['stations']
        elif field == 'fueltype':
            df = self.data['prices']
        df_merged = pd.merge(df_map, df, how='right', on=field)
        if df_merged[df_merged['db ' + field].isnull()].empty:
            df_merged = df_merged.iloc[:, 1:]
            df_merged = df_merged.rename(columns={'db ' + field: field})
        else:
            'alert user the mapping table needs to be updated'
            print(df_merged[df_merged['db ' + field].isnull()][[field, 'db ' + field]])
            df_merged['db ' + field].fillna(df_merged[field], inplace=True)

        if field == 'brand':
            self.data['stations'] = df_merged
        elif field == 'fueltype':
            self.data['prices'] = df_merged

map_file = 'W:\\RESEARCH\\Personal Folders\\Jeremy\\WebScraping\\FuelPrices\\brand_fueltype_map.xlsx'
fp_wa = FuelPrices_WA()
fp_nsw = FuelPrices_NSW()
fp_qldvic = FuelPrices_QLDVIC()
scripts = [fp_nsw, fp_wa, fp_qldvic]
for script in scripts:
    w = WebScraping(script)
    w.execute_script()
    w.standardize_names(map_file, 'fueltype')
    w.standardize_names(map_file, 'brand')
    w.save_to_csv()
