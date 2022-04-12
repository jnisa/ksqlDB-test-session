
CREATE TABLE event_v2_data
  (event_id VARCHAR,
    flow_id VARCHAR,
    transaction_id VARCHAR,
    transaction_lifecycle_event VARCHAR,
    created_at VARCHAR,
    error_details_source VARCHAR,
    error_details_message VARCHAR,
    error_details_decline_type VARCHAR,
    error_details_decision_type VARCHAR,
    error_details_decline_reason VARCHAR,
    error_details_decline_reason_v2 VARCHAR)
  WITH (KAFKA_TOPIC = '',
    VALUE_FORMAT = 'JSON',
    KEY = 'id')