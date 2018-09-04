import pandas as pd
from fuelprices_nsw import FuelPrices_NSW

class WebScraping():
    '''initialize with a script class'''

    def __init__(self, script):
        self.data = {}
        self.script = script
        self.files = []
        self.archive_folder = 'W:\RESEARCH\Personal Folders\Jeremy\WebScraping\FuelPrices\Archive'

    def save_to_csv(self, data):
        '''save dictionary of dataframes as csv files'''

    def insert_to_database(self, files):
        ''''upload csv file to database'''

    def execute_script(self):
        '''execute script and return a dictionary of dataframes'''
        data = self.script.main()

    def map_brands(self, data, map_file):
        '''standardize brand names'''

    def map_fueltype(self, data, map_file):
        '''standardize fueltype codes'''

fp_nsw = FuelPrices_NSW()
w = WebScraping(fp_nsw)
w.execute_script()
