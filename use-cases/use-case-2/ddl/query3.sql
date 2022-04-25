CREATE TABLE all_stream_info_agg AS
    SELECT
        USERID,
        SUM(CAST(DURATION AS BIGINT)) AS TOTAL_DURATION
    FROM all_stream_info_rekeyed
    GROUP BY USERID
    EMIT CHANGES;