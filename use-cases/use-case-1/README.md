## **Use Case 1 - Data Engineer Challenge**

### **1. Introduction**

The concept behind this first use case is to replicate the Primer Data Engineer Challenge but this time, by leveraging some of the concepts studied during the ksql courses.

### **2. Environment**

Following what was stated on the previous section and in order to use ksql on the proceedings, a docker container was created. This container comprises the following images:

- **zookeeper** node: that is responsible for the maintenance of the ecosystem configurations;
- **ksqldb** client and server: these will be the main pillars of the ksql service;
- **kafka** broker: that underlying technology of the one previously mentioned.

These multiple elements highlighted above interact with eachother according to the following flow:

![alt text for the image](../../images/container.png "Docker container")

### **3. Depedencies**

In addition to what was stated above, it is important to mention that to perform the interactions with ksqldb, a python wrapper was used. 

In order to enable it, we had to install the ksql python library on the broker node. This was made throuhgout the following command:

````
pip3 install ksql
````

**NOTE**: This modification must be commited in order to add this library to the docker image.

### **4. Minor Fixes**

The Environment described above levarages `confluentinc` images, however there's a minor detail that must be highlighted.

On the broker side, an adaptation needs to be made in order to mitigate a failure that resides on the library source code. Whenever a new insertion of data in a table was performed, errors from ksql are raised, to workaround it (I have checked the ksql repo and it is a topic that will be solved on the next version), modifications on the `api.py` were needed. I have made those changes and added the correct python script to this repo with the exact same name.

This script must be then copied to the broker's image where it will be used, and for that matter we have used the following command:

````
docker cp /path/to/the/project/ksqlDB-test-session/use-cases/use-case-1/api.py [CONTAINER_ID]:/usr/local/lib/python3.6/site-packages/ksql/
````

Please bear in mind, that this script must replace the one already existent.

After the steps highlighted in the last two sections, the environment can be considered up to the taks that this use case requires.

**NOTE**: This modification must be commited in order to add this library to the docker image.

### **5. Use Case Keypoints**

To solve this use case, the following tasks were perfomed:

1. Development of ksql client with the python wrapper already mentioned. This wrapper can be used to the next use cases and it allows the following DB actions: 1) Create Materialized Views, 2) Create Streams, 3) Create Tables, and 4) Insert records;
2. A set of ddls to perform queries that perform joins either between two tables or a table and a stream.

### **6. Approach**

In order to tackle this challenge, we have made the following steps:

1. Three of the four dimensions were added to the solution's pipeline as tables, the remaining dimension (`event_v2_data.csv`) was used to mock streaming events of the data;
2. Before the triggering the streaming data mock already mentioned, we must not only insert data into the dimensions mentioned in the previous point (`transaction.csv`, `transaction_request.csv`, and `payment_instrument_token_data.csv`) but also create the queries that will enable the joins between the tables and the stream. This will make sure that when new data is inserted into the pipeline, this data gets joined with the parametrization tables.

### **7. Proof of the final solution**

The proof that everything perfomed as expected must be a dimension with <u>**529 records**</u>. In this case, instead of a dimension we have a stream, and the proof that everything worked as expected, is the following command and output:

````
ksql> DESCRIBE THIRD_JOIN EXTENDED;
[...]
Runtime statistics by host
-------------------------
 Host               | Metric           | Value      | Last Message             
-------------------------------------------------------------------------------
 ksqldb-server:8088 | messages-per-sec |          0 | 2022-04-18T16:23:21.761Z 
 ksqldb-server:8088 | total-messages   |        529 | 2022-04-18T16:23:21.761Z 
-------------------------------------------------------------------------------
(Statistics of the local KSQL server interaction with the Kafka topic THIRD_JOIN)
[...]
````


### **A. Points to retain**

> a. The python wrapper needs some further improvements, but it can be useful to keep things as "pythonic" as possible. A point that is worth mentioning is the fact that this wrapper can be very peaky in what concerns the syntax of the query used;

> b. Table-Stream Joins are not supported, only Stream-Table Joins;

> c. It's mandatory to promote a column - whenever a new table is created - as the PRIMARY KEY on the query that creates the table;

> d. Don't create multiple tables allocated to the same kafka topic, that will impact the joining operations. One topic per table;

> e. Don't manage kafka topics (creation, deletion and so on..) on the kafka broker, do it through the ksql client.