


def create_mt_views(mt_view_id: str, sub_query: str) -> str:

    '''
    creates a materialized view on ksqlDB

    :param mt_view_id: id for the materialized view that will be created
    :param sub_query: query used by the materialized view
    '''

    query = '''CREATE TABLE %s AS %s EMIT CHANGES;''' %(mt_view_id, sub_query)

    return query


def create_stream(stream_id: str, columns: tuple, dtypes: tuple, topic: str, in_format: str, parts: int, add_fts = '') -> str:

    '''
    create a stream on the ksqlDB 

    :param stream_id: id of the stream to be created
    :param columns: tuple with the column names
    :param dtypes: tuple with the data types of the columns
    :param topic: id of the Kafka topic
    :param in_format: input format of the data
    :param parts: number of partitions of the stream
    :param add_fts: additional features to be added to the stream
    '''

    q_col = []

    for val in zip(columns, dtypes):
        q_col.append(' %s %s ' %(val[0], val[1]))

    query = '''CREATE STREAM IF NOT EXISTS %s (%s) WITH (KAFKA_TOPIC = '%s', VALUE_FORMAT='%s', PARTITIONS = %s %s);''' %(stream_id, ','.join(q_col), topic, in_format, parts, add_fts)

    return query


def create_table(table_id: str, columns: tuple, dtypes: tuple, topic: str, in_format: str, partitions: int, key_col: str,) -> str:

    '''
    creates a table on the ksqlDB

    :param table_id: id of the table to be created
    :param columns: tuple with the column names 
    :param dtypes: tuple with the column data types
    :param topic: kafka topic where the table will be created
    :param in_format: format of the input data
    :param partitions: number of kafka partitions
    :param key_col: key column from the input
    '''

    q_col = []

    for val in zip(columns, dtypes):
        if val[0] == key_col:
            q_col.append(' %s %s PRIMARY KEY' %(val[0], val[1]))
        else:
            q_col.append(' %s %s ' %(val[0], val[1]))

    query = '''CREATE TABLE IF NOT EXISTS %s (%s) WITH (KAFKA_TOPIC='%s', PARTITIONS=%s, VALUE_FORMAT='%s');''' %(table_id, ','.join(q_col), topic, partitions, in_format)

    return query


def insert_values(table_id: str, columns: tuple, values: tuple) -> str:

    '''
    inserts values on an existing kslq table

    :param table_id: id of the table that will be updated
    :param columns: tuple with the columns names
    :param values: tuple with the column values
    '''

    query = "INSERT INTO %s (" %(table_id) + ", ".join(columns) + ")  VALUES %s;" %(str(values))

    return query

