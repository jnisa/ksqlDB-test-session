CREATE STREAM IF NOT EXISTS points_transaction_log_rekeyed 
    WITH (KAFKA_TOPIC = 'points_transaction_log_rekeyed') AS
    SELECT *
    FROM points_transaction_log
    PARTITION BY USERID;