

. Extraction of the data to json or csv formats came is returned in an horrible format that needs further identation;
. No comparisons with NULL values on a WHERE clause use IT NOT NULL as a comparison operator;
. Always maintain the key that's on the join expression, otherwise you will find errors;
. Stream-Stream Joins must have a WITHIN clause;
. KSQL topic is different concept than Kafka topic. KSQL topic is an internal concept for KSQL that represents a kafka topic along with metadata about that topic including the topic format. Since we do not expose KSQL topic externally you should not use it in KSQL statements. If you wanna delete a kafka topic, you should delete it from kafka. In future we plan to add topic management capability to KSQL.
. please don't delete a topic on the kafka broker before deleting a table/stream that is using it 
. whenever you want to drop a stream, please use the following command
````
DROP STREAM [STREAM_NAME] DELETE TOPIC;
````
this will also help on the topic management, which can became a bit painful in the long-run
