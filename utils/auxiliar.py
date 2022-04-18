

import os



def read_sql(joins_dir: str, ddl: str) -> str:

    '''
    read a sql file and extracts the query to a python string

    :param joins_dir: directory where the .sql files are placed
    :param ddl: file that handles the necessary queries
    '''

    f = open(os.path.join(joins_dir, ddl))
    sql_join = f.read().replace('\n', ' ')
    f.close()

    return sql_join