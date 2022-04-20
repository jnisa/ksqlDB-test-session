
import pdb
import os
import json
import time

# from ksql import KSQLAPI

from utils.converter import csv_to_dict, json_creator
from utils.disruptor import get_sample, get_schema, get_records
from utils.auxiliar import read_sql
from client.ksql import (create_mt_views,
    create_stream,
    create_table, 
    insert_values
    )


# get a ksql client
# client = KSQLAPI('http://ksqldb-server:8088')

# getting the current directory
cur_dir = os.getcwd()

# universal variables definition
source = ['data', '1-raw-data']
landing = ['data', '2-curated-data']
data_format = 'JSON'


# configuration files
conf_path = os.path.join('/'.join(cur_dir.split('/')[:-2]), 'confs')

f = open(os.path.join(conf_path, 'py_to_kafka.json'))
map = json.load(f)

c = open(os.path.join(conf_path, 'use-case-2', 'convertion_map.json'))
features = json.load(c)


# convertion lifecyle application
for key in iter(features):
    recs = csv_to_dict(key, cur_dir, source)
    json_creator(cur_dir, landing, recs, features[key]['output'])

# create the ksql stream for the streaming dimension
vals = {}

for v in [v[1]['output'] for v in features.items()]:
    cols, dtyp = get_schema(get_sample(os.path.join(cur_dir, '/'.join(landing), v)), map)
    stream_vals = get_records(os.path.join(cur_dir, '/'.join(landing), v))
    # client.ksql(create_stream(v[:-5], cols, dtyp, v[:-5], data_format, 1))
    vals[v[:-5]] = stream_vals

# mock a data streaming process with the values collected previously

