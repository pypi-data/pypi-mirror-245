import requests
import json
import pandas as pd
from enum import auto
from datetime import datetime
from tkinter import filedialog
import csv






# API Call Types
ALL = auto()
ALLTABLE = auto()
SINGLETABLE = auto()
MIN = auto()
MAX = auto()
AVG = auto()
QTY = auto()
OFFERS = auto()
MINTIME = auto()
MAXTIME = auto()
AVGTIME = auto()
QTYTIME = auto()
OFFERSTIME = auto()
SEARCH = auto()
HELP = auto()




class PokeAPI:
    def __init__(self):
        '''
        A high level class for interacting with the PokeMMO Hub API.


        example:
        api = API()
        api.GET(MIN, item='Pink Cat Ears')

        This call will return the minimum price for Pink Cat Ears.


        '''

        # Loading ID:NAME csv table
        self.item_data = pd.read_csv('ItemID.csv')
        self.item_name_ids = self.item_data.set_index('ItemID')['Name'].to_dict()




        ## API URL Variables ##

        # Base URL
        self.url_ = 'https://pokemmoprices.com/api/v2/items/'

        # All Items
        self._all_items = f'{self.url_}all'

        # Tables
        self._all_items_table = f'{self.url_}table'
        self._single_item_table = f'{self.url_}table/'

        # Graphs
        self._min_price = f'{self.url_}graph/min/' 
        self._max_price = f'{self.url_}graph/max/'
        self._avg_price = f'{self.url_}graph/avg/' 
        self._qty = f'{self.url_}graph/quantity/'          
        self._offers = f'{self.url_}graph/offers/'

        # Timespans
        self._min_timespan = f"{self.url_}{self._min_price}"
        self._max_timespan = f"{self.url_}{self._max_price}"
        self._avg_timespan = f"{self.url_}{self._avg_price}"
        self._qty_timespan = f"{self.url_}{self._qty}"
        self._offers_timespan = f"{self.url_}{self._offers}"

        # Search Item
        self._search_item = f"{self.url_}search/"

        # Assign Each CallType a the corresponding URL Link
        self.call_urls = {  ALL: self._all_items,
                            ALLTABLE: self._all_items_table,
                            SINGLETABLE: self._single_item_table,
                            MIN: self._min_price,
                            MAX: self._max_price,
                            AVG: self._avg_price,
                            QTY: self._qty,
                            OFFERS: self._offers,
                            MINTIME: self._min_timespan,
                            MAXTIME: self._max_timespan,
                            AVGTIME: self._avg_timespan,
                            QTYTIME: self._qty_timespan,
                            OFFERSTIME: self._offers_timespan,
                            SEARCH: self._search_item
                        }


    def unix_2_dt(self, unix_timestamp):
        '''
        Converts the UNIX timestamp to a more user-friendly timestamp(for internal use)
        '''
        dt_object = datetime.utcfromtimestamp(unix_timestamp)
        return dt_object.strftime('%m-%d-%Y@%H:%M:%S')


    def enum_2_str(self, call_type):
        '''
        Converts the call_type enum to a string(for internal use)
        '''
        if call_type == ALL:
            return "ALL"
        elif call_type == ALLTABLE:
            return "ALLTABLE"
        elif call_type == SINGLETABLE:
            return "SINGLETABLE"
        elif call_type == MIN:
            return "MIN"
        elif call_type == MAX:
            return "MAX"
        elif call_type == AVG:
            return "AVG"
        elif call_type == QTY:
            return "QTY"
        elif call_type == OFFERS:
            return "OFFERS"
        elif call_type == MINTIME:
            return "MINTIME"
        elif call_type == MAXTIME:
            return "MAXTIME"
        elif call_type == AVGTIME:
            return "AVGTIME"
        elif call_type == QTYTIME:
            return "QTYTIME"
        elif call_type == OFFERSTIME:
            return "OFFERSTIME"
        elif call_type == SEARCH:
            return "SEARCH"
        elif call_type == HELP:
            return "HELP"



    def GET(self, call_type, item_name=None, item_id=None, time_span=None, save_csv=False, date_as_unix=False):
        '''
        For calling the specific type of GET to the PokeMMO Hub API
        Call types to the api can be any of the following types:

        ALL             * this returns a list of all items and thier ids 
        ALLTABLE        * this returns all of the items' infos to a table
        SINGLETABLE     *
        MIN             * returns minimum price of an item at a given time
        MAX             * returns minimum price of an item at a given time
        AVG             * returns average price of an item at a given time
        QTY             * returns number of a specified item available for sale on the gtl
        OFFERS          *
        MINTIME         *
        MAXTIME         *
        AVGTIME         *
        QTYTIME         *
        OFFERSTIME      *
        SEARCH          *
        HELP            * prints a neatly orgianized list of items and thier ids


        '''
        if call_type == HELP:
            for item_id, item_name in self.item_name_ids.items():
                print(f"ID: {item_id}, Name: {item_name}")
            return

        # Auto conversion of the item_id and item_name for ease of use
        if item_id != None and item_name == None:
            item_name = self.get_item_name(item_id)

        if item_name != None and item_id == None:
            item_id = self.get_item_id(item_name)

        # Checking The call type and constructing final url
        if call_type in [MIN,MAX,AVG,QTY,SINGLETABLE,OFFERS]:
            url = f'{self.call_urls[call_type]}{item_id}'

        elif call_type in [MINTIME,MAXTIME,AVGTIME,QTYTIME,OFFERSTIME]:
            url = f'{self.call_urls[call_type]}/{item_id}/{time_span}'
        
        elif call_type == SEARCH:
            url = f'{self._search_item}{item_name}'

        else:
            url = self.call_urls[call_type]

        # Make API call to URL
        response = requests.get(url)

        # Check the response status
        if response.status_code == 200:
            converted_data = []
            print('Get Succeess...')
            result = response.json()
            data = result['data']
            for each in data:
                converted = {}
                if call_type not in [ALL, ALLTABLE]:
                    data_name = item_name
                else:
                    data_name = each['n']
                if date_as_unix == False:
                    dt = self.unix_2_dt(each['x'])
                else:
                    dt = each['x']
                value = each['y']
                converted['Item'] = f'{data_name}'
                converted['Date'] = f'{dt}'
                converted['Value'] = value
                converted_data.append(converted)

            if save_csv:
                # Specify the CSV file path
                file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

                # Specify the field names (headers)
                fieldnames = ['Item', 'Date', 'Value']

                # Open the CSV file for writing
                with open(file_path, 'w', newline='') as csvfile:
                    # Create a CSV writer object
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    # Write the header to the CSV file
                    writer.writeheader()

                    # Write the data to the CSV file
                    writer.writerows(converted_data)

            return converted_data

        else:
            print(f'\n{url}')
            print(f'Error! GET returned with a    RESPONSE:{response.status_code}\n')





    def get_item_id(self, item_name):
        '''
        Gets the item id from the items name
        '''
        return self.item_name_ids.get(item_name)


    def get_item_name(self, item_id):
        '''
        Gets the item name from the items id
        '''        
        return self.item_name_ids.get(item_id)





# Example Functionality
if __name__ == '__main__':

    api = PokeAPI()
    info = api.GET(MIN, item_id=3360, save_csv=False, date_as_unix=True)
    print(info)
    api.get_item_id('Lure')
    api.GET(HELP)