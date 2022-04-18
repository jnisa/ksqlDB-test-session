

import json


def get_sample(file: str) -> dict:

    '''
    gets the first record of a json file

    :param file: json file 
    '''
    
    json_file = open(file)
    data = json.load(json_file)
    
    return data[0]


def get_schema(sample: dict, map: dict) -> list:

    '''
    from a data a sample this methods outputs the columns and the data types associated to it

    :param sample: data sample from obtained from a json file
    :param map: dict that establishes the correspondences between SQL and python
    '''


    cols = list(sample.keys())
    dtypes = [map[str(type(v)).replace("'>", "").replace("'", "").split(" ")[1]] for v in list(sample.values())]

    return cols, dtypes


def get_records(file: str) -> list:

    '''
    gets all the record values from a file

    :param file: json file
    '''

    json_file = open(file)
    data = json.load(json_file)

    return tuple(tuple(r.values()) for r in data)