#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-01-23 14:45:33

import redis, os, re, time
REDIS_HOST = '192.168.1.188'
REDIS_PORT = 6379
REDIS_DB = 0
NUMBER_LIST = 'number_list'
GPS_LIST = 'gps_list'
SWITCH_LIST = 'switch_list'
DATA_DIR = '/home/wangx/Documents/DjangoCode/zettage/appapi/appdata/'
global redis_connector
redis_connector = redis.StrictRedis(host=REDIS_HOST, port = REDIS_PORT, db = REDIS_DB)
def redis_to_file_num():
    global redis_connector
    while True:
        try:
            result = redis_connector.blpop(NUMBER_LIST,0)
            text = result[1].decode('utf8')
            sensor_id, stamp, value = text.split(',')
            file_path = os.path.join(DATA_DIR,sensor_id)
            file = open(file_path,'a')
            file.write('{0},{1}\n'.format(stamp,value))
            file.close()
        except:
            try: redis_connector = redis.StrictRedis(host=REDIS_HOST, port = REDIS_PORT, db = REDIS_DB)
            except: time.sleep(60)

def redis_to_file_switch():
    global redis_connector
    while True:
        try:
            result = redis_connector.blpop(SWITCH_LIST,0)
            text = result[1].decode('utf8')
            sensor_id, stamp, value = text.split(',')
            file_path = os.path.join(DATA_DIR,sensor_id)
            file = open(file_path,'a')
            file.write('{0},{1}\n'.format(stamp,value))
            file.close()
        except:
            try: redis_connector = redis.StrictRedis(host=REDIS_HOST, port = REDIS_PORT, db = REDIS_DB)
            except: time.sleep(60)

def redis_to_file_gps():
    global redis_connector
    while True:
        try:
            result = redis_connector.blpop(GPS_LIST,0)
            text = result[1].decode('utf8')
            sensor_id, stamp, value = re.match(r'([\d]*),([\d]{2,4}-[\d]{0,2}-[\d]{0,2}\s[\d]{1,2}:[\d]{1,2}:[\d]{1,2}),([\s\S]*)',text).groups()
            file_path = os.path.join(DATA_DIR,sensor_id)
            file = open(file_path,'a')
            file.write('{0},{1}\n'.format(stamp,value))
            file.close()
        except:
            try: redis_connector = redis.StrictRedis(host=REDIS_HOST, port = REDIS_PORT, db = REDIS_DB)
            except: time.sleep(60)
