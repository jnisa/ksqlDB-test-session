# ksqlDB-test-session
Repo that will handle some basic and practical exercises with ksqlDB

### 1. Overview

The idea behind this repo, is to create a testing stage for ksqlDB. A .json file will be the center of attentions on this repo, and in it we can find four data dimensions: 1) `event_v2_data`, 2) `transaction`, 3) `transaction_request`, and 4) `payment_instrument_token_data`.

We will use these dimensions to "stream them" (since it will be a python function taking care of the emulation of this streaming procedure) into 4 different streams. From that, some transformation operations will be made and also some joins in order to reach to the desired subsets of data (these will be defined in the meantime).

### 2. ksqlDB

To this _testing stage_ we will use a Docker container with Kafka installed on it, and a python wrapper to the ksqlDB API, that will allow the interaction with this tool to be more familiar and easy for a person with some knowledge on python.

### 3. Dependencies

It is important to take care of the installation of the next modules:

### . Create a Kafka Topic and create a table from it

Access to the Kafka server throughout the following command:

````
docker exec -it --priviliged --user root [CONTAINER_ID] /bin/sh
````

Inside the docker container, create a topic throughout the following command:

````
kafka-topics --bootstrap-server localhost:29092 --create --if-not-exists --topic my-topic-1 --replication-factor 1 --partitions 1
````

We have created the topic with random features, this must be brought into consideration before the creation moment.

With a kafka topic created, we can now create a table and add records to it throughout the following commands:

````
CREATE TABLE riderLocations
    (profile VARCHAR PRIMARY KEY,
    latitude DOUBLE
    longitude DOUBLE)
   WITH (KAFKA_TOPIC = 'my-topic-1', VALUE_FORMAT='JSON');

INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('c2309eec', 37.7877, -122.4205);
INSERT INTO riderLocations (profileId, latitude, longitude) VALUES ('18f4ea86', 37.3903, -122.0643);
````


