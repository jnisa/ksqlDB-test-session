# create the tables with ksql - pay attention to the maps between fields on the challenge documentation
    # 1. divide the ddl folder into a first level call setup (that will create the tables and the streams) 
    # 2. fill the tables with records from the csv's files

# setup the streaming data - put the streaming working to a test topic


import sys
sys.path.append("../..")

from utils.converter import csv_to_dict, json_creator

path = ['Users', 'joao.nisa', 'Desktop', 'Projects', 'personal', 'ksqlDB-test-session', 'use-cases']

use_case = 'use-case-1'
subpath = ['data', '1-raw-data']
out_subpath = ['data', '2-curated-data']

csv_to_convert = {
    'event_v2_data.csv': 'event_v2_data.json',
    'payment_instrument_token_data.csv': 'payment_instrument_token_data.json',
    'transaction_request.csv': 'transaction_request.json',
    'transaction.csv': 'transaction.json'
}


recs = csv_to_dict(path, list(csv_to_convert.keys())[0], use_case, subpath)
json_creator(path, use_case, out_subpath, recs, list(csv_to_convert.values())[0])

