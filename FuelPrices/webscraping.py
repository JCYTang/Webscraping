from datetime import datetime
from fuelprices_nsw import FuelPrices_NSW
from fuelprices_wa import FuelPrices_WA
from fuelprices_qldvic import FuelPrices_QLDVIC
import pandas as pd
import pyodbc
import os
import logging

class WebScraping():
    '''initialize with a script class'''

    def __init__(self, script):
        self.data = {}
        self.script = script
        self.files = {}
        self.archive_folder = '\\\\iml-fs-01\Work Data\\RESEARCH\\Personal Folders\\Jeremy\\WebScraping\\FuelPrices\\Archive'

    def save_to_csv(self):
        '''save dictionary of dataframes as csv files'''

        datestamp = datetime.today().strftime('%Y%m%d')
        stations_file = os.path.join(self.archive_folder, 'fuelstations_' + self.script.state + '.csv')
        prices_file = os.path.join(self.archive_folder, 'fuelprices_' + self.script.state + '_' + datestamp + '.csv')
        self.data['stations'].to_csv(stations_file, sep=';', index=False, header=False)
        self.data['prices'].to_csv(prices_file, sep=';', index=False, header=False)
        self.files['SP_ImportFuelStations'] = stations_file
        self.files['SP_ImportFuelPrices'] = prices_file

    def insert_to_database(self):
        ''''upload csv files to database'''

        server = 'imlvs03\sql2005'
        database = 'DW_Development'
        driver = '{SQL Server Native Client 11.0}'
        user = 'DWUser'
        password = 'gI7T@JD0rEdsF'
        conn = pyodbc.connect(uid=user, pwd=password, driver=driver, server=server, database=database)
        crsr = conn.cursor()
        for sp, filepath in self.files.items():
            sql = """DECLARE @rv VARCHAR(MAX);
            EXEC """ + sp + """ '""" + filepath + """', @rv OUTPUT;
            SELECT @rv AS return_value;"""
            crsr.execute(sql)
            return_value = crsr.fetchval()
            print(return_value)
            conn.commit()
        conn.close()

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
            unmapped_file = self.archive_folder + '\\unmapped.csv'
            df_merged[df_merged['db ' + field].isnull()][[field, 'db ' + field]].to_csv(unmapped_file, sep=',', index=False)

            df_merged['db ' + field].fillna(df_merged[field], inplace=True)
            df_merged = df_merged.iloc[:, 1:]
            df_merged = df_merged.rename(columns={'db ' + field: field})

        if field == 'brand':

            # #swap id and brand columns around
            id_col = df_merged['id']
            df_merged.drop('id', axis=1, inplace=True)
            df_merged.insert(0, 'id', id_col)
            self.data['stations'] = df_merged

        elif field == 'fueltype':
            self.data['prices'] = df_merged

if __name__ == "__main__":
    log_file = '\\\\iml-fs-01\\Work Data\\RESEARCH\\Personal Folders\\Jeremy\\WebScraping\\FuelPrices\\Archive\\log.log'
    logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO)

    map_file = '\\\\iml-fs-01\\Work Data\\RESEARCH\\Personal Folders\\Jeremy\\WebScraping\\FuelPrices\\brand_fueltype_map.xlsx'
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
        w.insert_to_database()
