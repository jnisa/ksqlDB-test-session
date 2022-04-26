
import pdb
import os
import json
import time

from ksql import KSQLAPI

from utils.converter import csv_to_dict, json_creator
from utils.disruptor import get_sample, get_schema, get_records
from utils.auxiliar import read_sql
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
stream_parts = 6 


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
cols = {}

for v in [v[1]['output'] for v in features.items()]:
    stream_cols, dtyp = get_schema(get_sample(os.path.join(cur_dir, '/'.join(landing), v)), map)
    stream_vals = get_records(os.path.join(cur_dir, '/'.join(landing), v))
    client.ksql(create_stream(v[:-5], stream_cols, dtyp, v[:-5], data_format, stream_parts))
    cols[v[:-5]] = stream_cols
    vals[v[:-5]] = stream_vals


# create the streams and tables with the window function
client.ksql('%s' %(read_sql(os.path.join(cur_dir, 'ddl'), 'query1.sql')))
client.ksql('%s' %(read_sql(os.path.join(cur_dir, 'ddl'), 'query2.sql')))
client.ksql('%s' %(read_sql(os.path.join(cur_dir, 'ddl'), 'query3.sql')))
client.ksql('%s' %(read_sql(os.path.join(cur_dir, 'ddl'), 'query4.sql')))

# create a stream with a timestamp column to use window functions
client.ksql('%s' %(read_sql(os.path.join(cur_dir, 'ddl'), 'query5.sql')))

pdb.set_trace()

# mock a data streaming process with the values collected previously
for k in vals.keys():
    for idx, v in enumerate(vals[k]):
        client.ksql(insert_values(k, tuple(cols[k]), v))

    print('The stream %s has values already!' %(k))

# run the queries that will allow us to get the expected outcomes
client.ksql('%s' %(read_sql(os.path.join(cur_dir, 'ddl'), 'outcome1.sql')))
# raising errors calling the query from here, but not when it comes directly from ksql client docker image
# client.ksql('%s' %(read_sql(os.path.join(cur_dir, 'ddl'), 'outcome2.sql')))