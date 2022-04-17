
-- CREATE FIRST JOIN TABLE (WORKING QUERY!)
SELECT P.TOKEN_ID, P.PAYMENT_INSTRUMENT_TYPE, P.VAULT_DATA, TR.FLOW_ID, TR.VAULT_OPTIONS_PAYMENT_METHOD
    FROM PAYMENT_INSTRUMENT_TOKEN_DATA P
    INNER JOIN TRANSACTION_REQUEST TR
    ON P.TOKEN_ID = TR.TOKEN_ID
    EMIT CHANGES
    LIMIT 3;
