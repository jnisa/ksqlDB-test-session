
import pdb
import os
import json

from ksql import KSQLAPI

from utils.converter import csv_to_dict, json_creator
from utils.disruptor import get_sample, get_schema, get_records
from utils.auxiliar import read_sql
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


# configuration files
conf_path = os.path.join('/'.join(cur_dir.split('/')[:-2]), 'confs')

f = open(os.path.join(conf_path, 'py_to_kafka.json'))
map = json.load(f)

c = open(os.path.join(conf_path, 'convertion_map.json'))
features = json.load(c)


# convertion lifecyle application
for key in iter(features):
    recs = csv_to_dict(key, cur_dir, source)
    json_creator(cur_dir, landing, recs, features[key]['output'])

# create the required tables with data
for t in list(features.keys()):
    cols, dtyp = get_schema(get_sample(os.path.join(cur_dir, '/'.join(landing), features[t]['output'])), map)
    vals = get_records(os.path.join(cur_dir, '/'.join(landing), features[t]['output']))
    client.ksql(create_table(t[:-4], cols, dtyp, t[:-4], data_format, 1, features[t]['primary_key']))

    for v in vals:
        client.ksql(insert_values(t[:-4], tuple(cols), v))


# perfom the joins
q1 = read_sql(os.path.join(cur_dir, 'ddl', 'setup'), 'join1.sql')
# q2 = read_sql(os.path.join(cur_dir, 'ddl', 'setup'), 'join2.sql')
# q3 = read_sql(os.path.join(cur_dir, 'ddl', 'setup'), 'join3.sql')

client.ksql('%s' %(q1.replace(';', '')))
# client.ksql('%s' %(q1.replace(';', '')))
# client.ksql('%s' %(q1.replace(';', '')))
