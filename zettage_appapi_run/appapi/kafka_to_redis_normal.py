#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-02-02 15:48:33


# Redis数据库信息
import redis, time
REDIS_HOST = '192.168.1.188'
REDIS_NORMAL_LIST = 'normal_list'
REDIS_PORT = 6379
REDIS_DB = 0

# kafka服务器信息
from kafka import KafkaConsumer
NORMAL_TOPIC = 'normal_topic'
global redis_connector
redis_connector = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB)
global kafka_consumer 
kafka_consumer = KafkaConsumer(NORMAL_TOPIC)
def kafka_to_redis_normal():
    global redis_connector
    global kafka_consumer
    while True:
        try:
            for msg in kafka_consumer:
                print('获取到了数据')
                print(msg)
                print(msg[4])
                redis_connector.rpush(REDIS_NORMAL_LIST,msg[4])
        except:
            try:
                redis_connector = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB)
                kafka_consumer = KafkaConsumer(NORMAL_TOPIC)
            except: time.sleep(60)

if __name__ == '__main__':
    kafka_to_redis_normal()
