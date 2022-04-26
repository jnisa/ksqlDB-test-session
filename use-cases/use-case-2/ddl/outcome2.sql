CREATE TABLE outcome2 AS
    SELECT
        USERID,
        SUM(CAST(POINTS AS BIGINT)) AS TOTAL_POINTS
    FROM points_transaction_log_rekeyed
    WINDOW TUMBLING (SIZE 4 HOURS) 
    GROUP BY USERID;
        