-- Queries used on the first ksql try-out

-- 1. Create a stream to the topic that has the source data
CREATE STREAM TRANSACTIONDB_DATA (DATA MAP<VARCHAR, VARCHAR>, METADATA MAP<VARCHAR, VARCHAR>) WITH (kafka_topic='transactiondb-cdc', partitions=6, value_format='JSON');

-- 2. Create all the dimensions needed in this case we need the following dimensions 
--      a. transaction_request
    CREATE STREAM TRANSACTION_REQUEST AS SELECT
        TRANSACTIONDB_DATA.DATA['flow_id'] AS FLOW_ID,
        TRANSACTIONDB_DATA.DATA['token_id'] AS TOKEN_ID,
        TRANSACTIONDB_DATA.DATA['vault_options'] AS VAULT_OPTIONS
    FROM TRANSACTIONDB_DATA TRANSACTIONDB_DATA
    WHERE (TRANSACTIONDB_DATA.METADATA['table-name'] = 'transaction_request')
    EMIT CHANGES;

--      b. payment_instrument_token_data
    CREATE STREAM PAYMENT_INSTRUMENT_TOKEN_DATA AS SELECT
        TRANSACTIONDB_DATA.DATA['token_id'] AS TOKEN_ID,
        TRANSACTIONDB_DATA.DATA['vault_data'] AS VAULT_DATA,
        TRANSACTIONDB_DATA.DATA['payment_instrument_type'] AS PAYMENT_INSTRUMENT_TYPE,
        TRANSACTIONDB_DATA.DATA['three_d_secure_authentication'] AS THREE_D_SECURE_AUTHENTICATION
    FROM TRANSACTIONDB_DATA TRANSACTIONDB_DATA
    WHERE (TRANSACTIONDB_DATA.METADATA['table-name'] = 'payment_instrument_token_data')
    EMIT CHANGES;

--      c. transaction
    CREATE STREAM TRANSACTION WITH (KAFKA_TOPIC='pksqlc-w1rwwTRANSACTION', PARTITIONS=6, REPLICAS=3) AS SELECT
        TRANSACTIONDB_DATA.DATA['transaction_id'] AS TRANSACTION_ID,
        TRANSACTIONDB_DATA.DATA['transaction_type'] AS TRANSACTION_TYPE,
        TRANSACTIONDB_DATA.DATA['amount'] AS AMOUNT,
        TRANSACTIONDB_DATA.DATA['currency_code'] AS CURRENCY_CODE,
        TRANSACTIONDB_DATA.DATA['processor_merchant_account_id'] AS PROCESSOR_MERCHANT_ACCOUNT_ID
    FROM TRANSACTIONDB_DATA TRANSACTIONDB_DATA
    WHERE (TRANSACTIONDB_DATA.METADATA['table-name'] = 'transaction')
    EMIT CHANGES;

--      d. event_v2_data
    CREATE STREAM EVENT_V2_DATA WITH (KAFKA_TOPIC='pksqlc-w1rwwEVENT_V2_DATA', PARTITIONS=6, REPLICAS=3) AS SELECT
        TRANSACTIONDB_DATA.DATA['event_id'] AS EVENT_ID,
        TRANSACTIONDB_DATA.DATA['flow_id'] AS FLOW_ID,
        TRANSACTIONDB_DATA.DATA['created_at'] AS CREATED_AT,
        TRANSACTIONDB_DATA.DATA['transaction_id'] AS TRANSACTION_ID,
        TRANSACTIONDB_DATA.DATA['transaction_lifecycle_event'] AS TRANSACTION_LIFECYCLE_EVENT,
        TRANSACTIONDB_DATA.DATA['ERROR_DETAILS'] AS ERROR_DETAILS
    FROM TRANSACTIONDB_DATA TRANSACTIONDB_DATA
    WHERE (TRANSACTIONDB_DATA.METADATA['table-name'] = 'event_v2_data')
    EMIT CHANGES;

--      e. processor_merchant_account_data
    CREATE STREAM PROCESSOR_MERCHANT_ACCOUNT_DATA AS SELECT
        TRANSACTIONDB_DATA.DATA['processor_id'] AS PROCESSOR_ID,
        TRANSACTIONDB_DATA.DATA['primer_account_id'] AS PRIMER_ACCOUNT_ID,
        TRANSACTIONDB_DATA.DATA['processor_merchant_account_id'] AS PROCESSOR_MERCHANT_ACCOUNT_ID
    FROM TRANSACTIONDB_DATA TRANSACTIONDB_DATA
    WHERE (TRANSACTIONDB_DATA.METADATA['table-name'] = 'processor_merchant_account_data')
    EMIT CHANGES;

-- 3. We are now in conditions to perform the query that will make us obtain the expected outcome
CREATE STREAM MERCHANT_METRICS_KAFKA AS
    SELECT
        tr.transaction_id,
        ed.event_id as id,
        tr.transaction_type,
        tr.amount,
        tr.currency_code,
        ed.flow_id,
        ed.created_at,
        tr.processor_merchant_account_id,
        ed.transaction_lifecycle_event,
        ed.error_details,
        pmad.processor_id as connection_name,
        pmad.primer_account_id,
        pitd.vault_data,
        pitd.payment_instrument_type,
        request.vault_options,
        request.token_id,
        pitd.three_d_secure_authentication
    FROM
        event_v2_data ed
        LEFT JOIN TRANSACTION tr WITHIN 1 HOUR ON ed.transaction_id = tr.transaction_id
        LEFT JOIN processor_merchant_account_data pmad WITHIN 1 HOUR ON tr.processor_merchant_account_id = pmad.processor_merchant_account_id
        LEFT JOIN transaction_request request WITHIN 1 HOUR ON request.flow_id = ed.flow_id
        LEFT JOIN payment_instrument_token_data pitd WITHIN 1 HOUR ON request.token_id = pitd.token_id
        EMIT CHANGES;

-- the index is automatically created with the name of the kafka topic, so the next steps are:
--   1. definition of a schema on the output topic
--   2. change the features of the elasticsearch connector

CREATE SINK CONNECTOR test_connector_1 WITH (
  'connector.class' = 'io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
  'topics'          = 'orders',
  'connection.url'  = 'http://elasticsearch:9200',
  'type.name'       = '_doc',
  'key.ignore'      = 'false',
  'schema.ignore'   = 'true'
);

{
  "name": "ElasticsearchSinkConnector_vtest",
  "config": {
    "topics": "merchant_metrics_kafka_test",
    "input.data.format": "AVRO",
    "connector.class": "ElasticsearchSink",
    "name": "ElasticsearchSinkConnector_0",
    "kafka.auth.mode": "KAFKA_API_KEY",
    "connection.url": "https://dev-reporting.es.eu-west-1.aws.found.io:9243",
    "connection.username": "jnisa",
    "batch.size": "1",
    "tasks.max": "1",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter"
  }
}

--   3. check the data in the ElasticSearch