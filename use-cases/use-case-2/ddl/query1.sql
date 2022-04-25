CREATE STREAM IF NOT EXISTS all_stream_info_rekeyed 
    WITH (KAFKA_TOPIC = 'all_stream_info_rekeyed') AS
    SELECT *
    FROM all_stream_info
    PARTITION BY USERID;