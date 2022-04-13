# CHECK THE KEYS NEEDED TO THE PERFORM THE JOINS 

# create the tables with ksql - pay attention to the maps between fields on the challenge documentation
    # 1. divide the ddl folder into a first level call setup (that will create the tables and the streams) 
    # 2. fill the tables with records from the csv's files

# setup the streaming data - put the streaming working to a test topic



import os
from utils.converter import csv_to_dict, json_creator


# getting the current directory
cur_dir = os.getcwd()

# use case, source and output directories definition
source = ['data', '1-raw-data']
landing = ['data', '2-curated-data']

# convertion map
csv_to_convert = {
    'event_v2_data.csv': ['event_id', 'event_v2_data.json']
    # 'payment_instrument_token_data.csv': ['' , 'payment_instrument_token_data.json'],
    # 'transaction_request.csv': ['' , 'transaction_request.json'],
    # 'transaction.csv': ['' , 'transaction.json']
}

# convertion lifecyle application
recs = csv_to_dict(list(csv_to_convert.keys())[0], cur_dir, source, list(csv_to_convert.values())[0][0])
json_creator(cur_dir, landing, recs, list(csv_to_convert.values())[0][1])

# create tables


# create stream