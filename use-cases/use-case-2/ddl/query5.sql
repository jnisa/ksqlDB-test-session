CREATE STREAM points_transaction_time_window
    WITH (KAFKA_TOPIC='points_transaction_time_window', partitions=6, timestamp='UTCTIMESTAMP', timestamp_format='yyyy-MM-dd HH:mm:ss') AS
    SELECT
        USERID,
        SUBSTRING(UTCTIMESTAMP, 0, 19) AS UTCTIMESTAMP,
        POINT
    FROM
        points_transaction_log_rekeyed;