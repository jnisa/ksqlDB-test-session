CREATE TABLE points_transaction_log_agg AS
    SELECT 
        USERID,
        SUM(CAST(POINT AS BIGINT)) AS TOTAL_POINTS
    FROM points_transaction_log_rekeyed
    GROUP BY USERID
    EMIT CHANGES;