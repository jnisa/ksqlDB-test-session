

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