

import subprocess 


def create_topic(topic_id: str, rep_factor: int, partitions: int, container: str):

    '''
    creates a Kafka topic with the required features

    :param topic_id: name of the topic that we want to create
    :param rep_factor: integer relative to the replication factor
    :param partitions: number of partitions that the topic will have
    :param container: kafka container id of the kafka broker 
    '''

    cmd_1 = 'docker exec %s' %(container)
    cmd_2 = 'kafka-topics --bootstrap-server localhost:29092 --create --if-not-exists --topic %s --replication-factor %s --partitions %s' %(topic_id, rep_factor, partitions)

    return subprocess.run(cmd_1.split(' ') + cmd_2.split(' '))


def remove_topic(topic_id: str, container: str):

    '''
    removes a Kafka topic created

    :param topic_id: name of the topic that will be deleted
    :param container: kafka container id of the kafka broker
    '''

    cmd_1 = 'docker exec -it --privileged --user root %s /bin/sh' %(container)
    cmd_2 = 'kafka-topics --bootstrap-server localhost:29092 --delete --topic %s ' %(topic_id)

    return subprocess.run(cmd_1.split(' ') + cmd_2.split(' '))