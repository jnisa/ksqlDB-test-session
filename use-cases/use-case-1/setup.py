

from client.kafka import create_topic


# create the kafka topics needed
create_topic('first-topic', 1, 1, 'broker')