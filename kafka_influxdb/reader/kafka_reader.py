# -*- coding: utf-8 -*-

import logging
import time

from pykafka import KafkaClient

class KafkaReader(object):
    def __init__(self, host, zookeeper,group, topic, partitions=None,reconnect_wait_time=2):
        """
        Initialize Kafka reader
        """
        self.host = host
        self.zookeeper = zookeeper
        self.group = group
        self.topic = topic
        self.reconnect_wait_time = reconnect_wait_time
        self.partitions=partitions
        # Initialized on read
        self.consumer = None

    def _connect(self):
        
        client = KafkaClient(hosts=self.host,zookeeper_hosts=self.zookeeper)
        topic = client.topics[self.topic]
        self.consumer = topic.get_balanced_consumer(
             consumer_group=self.group,
             auto_commit_enable=True,
             zookeeper_connect=self.zookeeper
        )
            
    @staticmethod
    def getHosts(host):
        ps=host.split(",")
        rs=[]
        for p in ps:
            rs.append(p)
        return rs
            
    
    @staticmethod
    def getpartitions(partitions):
        ps=partitions.split(",")
        rs=[]
        for p in ps:
            rs.append(int(p))
        return rs
    def read(self):
        """
        Read from Kafka. Reconnect on error.
        """
        while True:
            #print "start read:"+time.strftime("%Y-%m-%d %X", time.localtime())
            for msg in self._handle_read():
                yield msg

    def _handle_read(self):
        """
        Yield messages from Kafka topic
        """
        try:
            self._connect()
            for message in self.consumer:
                yield message.value
        except Exception as e:
            logging.error("Kafka error: %s.", e)
            logging.error("Trying to reconnect to %s:%s", self.host, self.port)
            time.sleep(self.reconnect_wait_time)
            pass
    def _handle_read_(self):
        """
        Yield messages from Kafka topic
        """
        try:
            self._simple_connect()
            for message in self.consumer:
                yield message.value
        except Exception as e:
            logging.error("Kafka error: %s.", e)
            logging.error("Trying to reconnect to %s:%s", self.host, self.port)
            time.sleep(self.reconnect_wait_time)
            pass
