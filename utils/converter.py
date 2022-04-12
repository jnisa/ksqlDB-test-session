
import pdb
import os
import csv
import json

def csv_to_dict(pre_path, in_csv: str, use_case: str, subpath: list, data = {}) -> dict:
    
    '''
    reads the records from the csv file and converts them to a python dictionary
    
    :param in_csv: name of the file that we want to convert each record
    :param use_case: name of the specific use_case
    :param subpath: subpath within the use case folder 
    '''

    with open('/' + os.path.join('/'.join(pre_path), use_case, '/'.join(subpath), in_csv)) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            
            # pdb.set_trace()
            
            id = rows['event_id']
            data[id] = rows

    return data


def json_creator(pre_path, use_case: str, subpath: list, records: dict, outfile: str):

    '''
    converts a set of python dictionaries into a json file

    :param use_case: name of the use case of the output json file
    :param subpath: intermediare path to get store path 
    :param records: set of python dictionaries to be converted
    :param outfile: name of the .json file that will handle all the records 
    '''

    with open(os.path.join('/' + '/'.join(pre_path), use_case, '/'.join(subpath), outfile), 'w') as json_file: 
        json_file.write(json.dumps(records, indent=4))
