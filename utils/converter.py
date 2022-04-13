

import os
import csv
import json



def csv_to_dict(csv_asset: str, path: str, locator: list, key_col: str, data = []) -> dict:
    
    '''
    reads the records from the csv file and converts them to a python dictionary
    
    :param csv_asset: name of the file that we want to convert each record
    :param path: location of the working directory
    :param locator: locator correspondent to the use location
    :param key_col: column from the data that will be used as key of the json 
    '''

    with open(os.path.join(path, '/'.join(locator), csv_asset)) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            data.append(rows)
            # id = rows[key_col]
            # data[id] = dict((key,value) for key, value in rows.items() if not key == key_col)

    return data


def json_creator(path: str, locator: list, records: dict, outfile: str):

    '''
    converts a set of python dictionaries into a json file

    :param path: location of the working directory
    :param locator: locator correspondent to the use location 
    :param records: set of python dictionaries to be converted
    :param outfile: name of the .json file that will handle all the records 
    '''

    with open(os.path.join(path, '/'.join(locator), outfile), 'w') as json_file: 
        json_file.write(json.dumps(records, indent=4))
