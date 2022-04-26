# ksqlDB-test-session
Repo that will handle some basic and practical exercises with ksqlDB

#### **Version Control**
[![Generic badge](https://img.shields.io/badge/ksql-0.10.2-blue)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/confluentinc%2Fzookeeper-7.0.1-green)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/confluentinc%2Fcp--kafka-7.0.1-green)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/confluentinc%2Fksql-0.24.0-green)](https://shields.io/)

### **1. Overview**

The idea behind this repo, is to create a testing stage for ksqlDB. A .json file will be the center of attentions on this repo, and in it we can find four data dimensions: 1) `event_v2_data`, 2) `transaction`, 3) `transaction_request`, and 4) `payment_instrument_token_data`.

We will use these dimensions to "stream them" (since it will be a python function taking care of the emulation of this streaming procedure) into 4 different streams. From that, some transformation operations will be made and also some joins in order to reach to the desired subsets of data (these will be defined in the meantime).

### **2. ksqlDB**

To this _testing stage_ we will use a Docker container with a Kafka broker installed on it, and a python wrapper to the ksqlDB API, that will allow the interaction with this tool to be more familiar and easy for a person with some knowledge on python.

Basically the Docker container used to address this challenge, comprises the following modules/images:

- **zookeeper** node: that is responsible for the maintenance of the ecosystem configurations;
- **ksqldb** client and server: these will be the main pillars of the ksql service;
- **kafka** broker: that underlying technology of the one previously mentioned.

These multiple elements highlighted above interact with eachother according to the following flow:

![alt text for the image](images/container.png "Docker container")

This will be the environment that is going to be used on all the use cases targeted.

### **3. Dependencies**

In order to keep things as "_pythonic_" as possible, we have added the the ksql module to the kafka broker. After getting access to the kafka broker console, the following command was performed

````
pip3 install ksql
````

This modifications were then committed to the kafka broker new image.

### **4. Project Tree**

This project is subdivided/organized into the following modules:

- [`/client`](/client/), where the ksql client was developed. This client leverages the python wrapper already mentioned and allows the user to perform the following actions on a ksql environment: 1) create materialized views, 2) create tables, 3) create streams, and 4) insert records. This last function can be used to insert values on tables but also on streams;

- [`/confs`](/confs/), where two configuration files can be found. The more generalistic one (`py_to_kafka.json`) is a file that essentially maps the data types from python to data types on SQL. The remaining one essentially establishes a correspondence between the .csv files provided to the .json files (that is a file type more "_ksql-friendly_") that are produced after using the `json_creator` method and the primary keys that each table/stream that must have;

- [`/images`](/images), a directory where all the images used on the documentation can be found;

- [`/notes`](/notes), a centralized unit where you can find some of the notes that I have collected during the confluent ksql courses;

- [`/use-cases`](/use-cases/), this directory essentially possesses all the uses cases that were developed to have a more practical perception of ksql capibilities. Two uses cases are on the scope:

> 1. `use-case-1` - that is essentially the data engineer challenge from Primer, but in this case we have to solve it by using ksql;

> 2. `use-case_2` [**TO BE COMPLETED**] - where the window functions capabilities are explored;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This module has also submodules, one dedicated to the queries used on the course of each use case (`/ddl`) and one to the data used in each challenge (`/data`).

- [`/utils`](/utils/), the storage unit of all the python auxiliar methods;  

### **5. Command to Trigger the ksql client**

The start the ksql client, we must use the following commmand:

````
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
````


### **A. Most used commands on the Kafka broker**

After getting access to the Kafka broker already mentioned above throughout the following command:

````
docker exec -it --priviliged --user root [BROKER_CONTAINER_ID] /bin/sh
````

The most used commands to interact with Kafka were the ones listed down below:

````
# 1. list the kafka topics
kafka-topics --bootstrap-server localhost:29092 --list

# 2. create a new kakfa topic
kafka-topics --bootstrap-server localhost:29092 --create --if-not-exists --topic [TOPIC_NAME] --replication-factor [REPLICATION_FACTOR] --partitions [PARTITIONS_NUMBER]

# 3. count the number of messages that a kafka topic possesses
kafka-run-class kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic [TOPIC_NAME] --time 1 --offsets 1 | awk -F ":" '{sum += $3} END {print sum}'
````

However, some of the commands highlighted above can be avoided by using the `DESCRIBE [STREAM_NAME] EXTENDED` command, that will clearly point out the number of messages on the stream, this specifically addresses the third command. Regarding the second one, it's important to mention that the creation of kafka topics must be made entirely by the ksql.

### **B. Points to retain/reflect**

- **On the Confluent Cloud side**
1. The extraction of the data to json or csv formats is returned in an ugly format that needs further indentation otherwise it's really difficult to make some fast analysis around the data;
2. Confluent Cloud is a bit restrictive concerning some of the connector features. As an example, whenever you create a connector, it is not possible to perform key or value converting options. To accomplish that I had to use the Confluent CLI;
3. It's not possible to create variables throughout the command `DEFINE test_var='test-123'`.

- **On the Confluent CLI**
1. The configurations that are not allowed to be performed to connectors, directly on the Confluent Cloud, can be performed throughout the CLI. After the installation of the Confluent CLI we can follow these steps,
````
--- create a .json file with the configurations that you want to apply
sh-3.2# cat conn_test.json
{
  "name": "ElasticsearchSinkConnector_0",
  "config": {
    "topics": "merchant_metrics_kafka_test",
    "input.data.format": "AVRO",
    "connector.class": "ElasticsearchSink",
    "name": "ElasticsearchSinkConnector_0",
    "kafka.auth.mode": "KAFKA_API_KEY",
    "connection.url": "https://dev-reporting.es.eu-west-1.aws.found.io:9243",
    "connection.username": "jnisa",
    "batch.size": "1",
    "tasks.max": "1",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.storage.StringConverter"
  }
}

--- check the connector id to whom you want to apply the configurations
sh-3.2# confluent connect list
      ID     |             Name             | Status  |  Type  | Trace
-------------+------------------------------+---------+--------+--------
  lcc-7yp11p | ElasticsearchSinkConnector_0 | PAUSED  | sink   |

--- apply the configuration file to the connector
sh-3.2# confluent connect update lcc-7yp11p --config conn_test.json

--- you can then check that your modifications were applied describing the connector
sh-3.2# confluent connect describe lcc-7yp11p 
````

- **On the ksql**
1. It's crucial to always highlight a key whenever you are creating tables or streams because that will be directly leveraged on join computations;
2. Stream-Stream joins must have a WITHIN clause. This will restrict the join operation to a specific time window, otherwise, it can be painful (depending on the volumetry) to join an all universe of data at once - which by the way is possible, but has to be specifically stated on the query;
3. Manage ksql topic can easily become a painful task. In some opinions, this management must be made directly from the Kafka broker, however by using ksql both on the docker container and Confluent Cloud I have concluded that the **best option** is to perform the following query whenever you decide to delete a stream or a table,
````
DROP STREAM/TABLE [STREAM/TABLE_NAME] DELETE TOPIC;
````
This query above will not only delete the stream or table but also delete the corresponding topic;
4. Substitution variable procedures allow string part substitutions if we're talking about some of the stream features (that are the arguments of the `WITH` clause) or complete subtitutions, but not if you want to do it on the name definition of a stream or table. To better illustrate this, let's consider the following code:
````
DEFINE random_variable='test-123'

--- it is not possible to do this
CREATE STREAM stream_${random_variable} WITH (KAFKA_TOPIC='test_topic')

--- it is possible to do this
CREATE STREAM stream WITH (KAFKA_TOPIC='stream_${random_variable}')

--- it is possible to do this
CREATE STREAM ${random_variable} WITH (KAFKA_TOPIC='stream_${random_variable})
````
5. ksql topic is a different concept than Kafka topic. ksql topic is an internal concept for ksql that represents a kafka topic along with metadata about that topic including the topic format;
6. Don't create multiple tables allocated to the same kafka topic, that will impact the joining operations. One topic per table;
7. Table-Stream Joins are not supported, only Stream-Table Joins;
8. Timestamp columns can have an impact on the `GROUP BY` and `WINDOW` operations. As an example, after the setting up the two streams on the [/use-case-2](/use-cases/use-case-2/) and elect the `beginTime` as a timestamp column, no data was arriving to the table that performs an aggregation to compute the total duration by userid. To sort this out, I had to separate this two steps.

- **On the ksql python wrapper used**
1. There are some bugs that are a bit unpleasent specially due to the fact that they rely in details. As an example, and looking to the [/use-case-2](/use-cases/use-case-2/) the query on the `outcome2.sql` file runs if you perform it on the ksql-client directly but it raises errors if you perform by using the python wrapper;
2. The python wrapper needs some further improvements, but it can be useful to keep things as "pythonic" as possible. A point that is worth mentioning is the fact that this wrapper can be very peaky in what concerns the syntax of the query used.


`Last update`: 02/05/2022