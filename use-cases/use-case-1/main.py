

import os
import json

from ksql import KSQLAPI

from utils.converter import csv_to_dict, json_creator
from utils.disruptor import get_sample, get_schema, get_records
from client.kafka import create_topic
from client.ksql import (create_mt_views,
    create_stream,
    create_table, 
    insert_values
    )

# get a ksql client
client = KSQLAPI('http://ksqldb-server:8088')

# getting the current directory
cur_dir = os.getcwd()

# universal variables definition
source = ['data', '1-raw-data']
landing = ['data', '2-curated-data']
data_format = 'JSON'

# map input files: output files
csv_to_convert = {
    'event_v2_data.csv': 'event_v2_data.json',
    'payment_instrument_token_data.csv': 'payment_instrument_token_data.json',
    'transaction_request.csv': 'transaction_request.json',
    'transaction.csv': 'transaction.json'
}

# convertion lifecyle application
for key in iter(csv_to_convert):
    recs = csv_to_dict(key, cur_dir, source)
    json_creator(cur_dir, landing, recs, csv_to_convert[key])

# data types map (between python and SQL)
path = cur_dir.split('/')[:-2]
f = open(os.path.join('/'.join(path), 'confs', 'py_to_kafka.json'))
map = json.load(f)

# create the required tables with data
for t in list(csv_to_convert.keys())[1::]:

    cols, dtyp = get_schema(get_sample(os.path.join(cur_dir, '/'.join(landing), csv_to_convert[t])), map)
    vals = get_records(os.path.join(cur_dir, '/'.join(landing), csv_to_convert[t]))

    # for test purposes we are forcing the 'token_id' as primary column
    if 'token_id' in cols:
        p_key = 'token_id'
    else: 
        p_key = cols[0]
    client.ksql(create_table(t[:-4], cols, dtyp, t[:-4], data_format, 1, p_key))
    for v in vals:
        client.ksql(insert_values(t[:-4], tuple(cols), v))


# create stream