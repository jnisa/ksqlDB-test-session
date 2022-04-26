CREATE TABLE outcome1 AS
    SELECT
        all_stream.USERID AS USERID,
        all_stream.TOTAL_DURATION AS TOTAL_DURATION,
        points_transaction.TOTAL_POINTS AS TOTAL_POINTS
    FROM all_stream_info_agg all_stream
    INNER JOIN points_transaction_log_agg points_transaction 
    ON all_stream.USERID = points_transaction.USERID;