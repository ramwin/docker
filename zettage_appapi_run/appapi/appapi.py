#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Xiang Wang @ 2016-01-04 11:43:05
import json, time, os, re
from flask import Flask
from flask import request
from flask import render_template
from functools import wraps
from flask import make_response
import requests
app = Flask(__name__)

class Log():
    def __init__(self,path):
        self.path = path
    def warning(self,text):
        print(text)
        self.files = open(self.path,'a')
        timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        self.files.write("[WARN][{time}] {text}\n".format(text=normal_str(text),time=timestr))
        self.files.close()
    def info(self,text):
        print(text)
        self.files = open(self.path,'a')
        timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        self.files.write("[INFO][{time}] {text}\n".format(text=normal_str(text),time=timestr))
        self.files.close()
    def error(self,text):
        print(text)
        self.files = open(self.path+'.err','a')
        timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        self.files.write("[ERR ][{time}] {text}\n".format(text=normal_str(text),time=timestr))
        self.files.close()

log = Log('./log/appapi.log')
AUTHURL = 'http://192.168.1.88/device/apiauth'

APP_DATA_DIR = '/home/wangx/Documents/DjangoCode/zettage/appapi/appdata'

# 使用kafka信息
from kafka import SimpleProducer, SimpleClient
KAFKA_SERVER = "192.168.1.190:9092"
NUMBER_TOPIC = "number_topic"
GPS_TOPIC = "gps_topic"
NORMAL_TOPIC = 'normal_topic'
SWITCH_TOPIC = 'switch_topic'
global kafka_client
global kafka_producer
kafka_client = SimpleClient(KAFKA_SERVER)
kafka_producer = SimpleProducer(kafka_client, async=False)

# ---------------------------数据库类-----------------
class Gps():
    def __init__(self, timevalue, value, sensor_id):
        self.time = timevalue
        self.value = value
        self.sensor_id = sensor_id
        self.data = '{0},{1},{2}'.format(self.sensor_id, self.time, self.value)
    def binvalue(self):
        return self.data.encode('utf-8')
    def save(self):
        '''存入数据,成功True,失败False'''
        if self.illegal(): return False
        global kafka_client
        global kafka_producer
        try: kafka_producer.send_messages(GPS_TOPIC,self.binvalue())
        except: 
            try:
                kafka_client = SimpleClient(KAFKA_SERVER)
                kafka_producer = SimpleProducer(kafka_client, async=False)
                kafka_producer.send_messages(GPS_TOPIC,self.binvalue())
            except:
                return False
        return True
    def illegal(self):
        '''成功 False 失败 True'''
        if re.match(r'^[0-9.{}xyv,\s\"\':]*$',self.data): return False
        return True
       
class Normal():
    def __init__(self,key,value, sensor_id):
        self.key = key
        self.value = value
        self.sensor_id = sensor_id
        self.data = '{0},{1},{2}'.format(self.sensor_id,self.key,self.value)
    def binvalue(self):
        return self.data.encode('utf-8')
    def save(self):
        '''存入数据,成功True,失败False'''
        if self.illegal(): return False
        global kafka_client
        global kafka_producer
        try:kafka_producer.send_messages(NORMAL_TOPIC,self.binvalue())
        except:
            try:
                kafka_client = SimpleClient(KAFKA_SERVER)
                kafka_producer = SimpleProducer(kafka_client, async=False)
                kafka_producer.send_messages(NORMAL_TOPIC,self.binvalue())
            except:
                return False
        return True
    def illegal(self):
        '''成功: False, 失败: True'''
        has_enter =  b'\n' in self.binvalue() # 不得有换行符
        return has_enter

class Number():
    def __init__(self,timevalue,value,sensor_id):
        self.time = timevalue
        self.value = value
        self.sensor_id = sensor_id
        self.data = '{0},{1},{2}'.format(self.sensor_id,self.time,self.value)
    def binvalue(self):
        return self.data.encode('utf-8')
    def save(self):
        '''存入数据,成功True,失败False'''
        if self.illegal(): return False
        global kafka_client
        global kafka_producer
        try:kafka_producer.send_messages(NUMBER_TOPIC,self.binvalue())
        except:
            try:
                kafka_client = SimpleClient(KAFKA_SERVER)
                kafka_producer = SimpleProducer(kafka_client, async=False)
                kafka_producer.send_messages(NUMBER_TOPIC,self.binvalue())
            except:
                return False
        return True
    def illegal(self):
        '''数据认证,成功返回False, 失败返回True'''
        log.info('illegal')
        try: 
            tmp = float(self.value)
            log.info('认证成功')
        except: return True
        return False

class Switch():
    def __init__(self,timevalue,value,sensor_id):
        self.time = timevalue
        self.value = value
        self.sensor_id = sensor_id
        self.data = '{0},{1},{2}'.format(self.sensor_id,self.time,self.value)
    def binvalue(self):
        return self.data.encode('utf-8')
    def save(self):
        '''存入数据,成功True,失败False'''
        if self.illegal(): return False
        global kafka_client
        global kafka_producer
        try:kafka_producer.send_messages(SWITCH_TOPIC,self.binvalue())
        except:
            try:
                kafka_client = SimpleClient(KAFKA_SERVER)
                kafka_producer = SimpleProducer(kafka_client, async=False)
                kafka_producer.send_messages(SWITCH_TOPIC,self.binvalue())
            except:
                return False
        return True
    def illegal(self):
        '''数据认证,成功返回False, 失败返回True'''
        log.info('illegal')
        try: 
            tmp = int(self.value)
            if tmp not in (1,0): return True
            log.info('认证成功')
        except: return True
        return False

# ---------------------------通用函数------------------
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun
    
def normal_str(string):
    if isinstance(string, str):
        return string
    elif isinstance(string, unicode):
        return string.encode('utf-8')
        
def authenticate(apikey, device_id, sensor_id):
    '''直接给django发送请求进行认证
        成功: {'type':'number'}
        失败: False'''
    log.info('authenticate')
    url = AUTHURL
    response = requests.get(url, params={
        'sensor_id':sensor_id,'apikey':apikey})
    if response.status_code == 200:
        return json.loads(response.text)
    return False

# ---------------------------web请求-----------------
# 测试用
@app.route('/test/', methods=["GET"])
def test():
    return render_template('test.html')
@app.route('/test2/', methods=["POST"])
def test2():
    value = request.json['value'] # 获取到的是str
    text = '汉字{0}'.format(value)
    print(type(text))
    print(type('汉字'))
    return json.dumps({'status':'success'}),200

# 上传数据
@app.route('/upload/v1.0/device/<device_id>/sensor/<sensor_id>/',methods=["POST"])
def uploaddata(device_id, sensor_id):
    log.info('获取了上传数据的请求')
    timevalue = request.json['time']
    log.info(timevalue)
    apikey = request.headers['apikey']
    authen = authenticate(apikey,device_id,sensor_id)
    if not authen: return json.dumps({'status':'failed'}), 401
    if authen['type']=='number':    # 认证
        log.info('number数据')
        value = request.json['value']
        number = Number(timevalue,value,sensor_id)
        if number.save():
            response = json.dumps({'status':'success'}),200
            log.info('数据已存入,uploaddata--成功')
            return response
        else:
            response = json.dumps({'status':'failed'}),500
            log.error('数据存入失败')
            return response
    elif authen['type'] == 'switch':
        value = request.json['value']
        switch = Switch(timevalue, value, sensor_id)
        if switch.save():
            response = json.dumps({'status':'success'}),200
            log.info('数据已存入,uploaddata--成功')
            return response
        else:
            response = json.dumps({'status':'failed'}),500
            log.error('数据存入失败')
            return response
    elif authen['type'] == 'gps':
        log.info('写入gps数据')
        value = request.json['value']
        gps = Gps(timevalue, value, sensor_id)
        if gps.save():
            return json.dumps({'status':'success'}),200
        else:
            response = json.dumps({'status':'failed'}),500
            log.error('数据存入失败')
            return response
    elif authen['type'] == 'normal':
        key = request.json['key']
        value = request.json['value']
        normal = Normal(key,value,sensor_id)
        if normal.save(): return json.dumps({'status':'success'}),200
        else:
            log.error('数据存入失败\nkey:\n{0}\nvalue:\n{1}'.format(key,value))
            return json.dumps({'status':'failed'}),500
        
            

# 获取传感器所有数据
@app.route('/getall/v1.0/device/<device_id>/sensor/<sensor_id>/', methods=["GET"])
@allow_cross_domain
def getalldata(device_id, sensor_id):
    log.info('获取所有数据')
    apikey = request.args['apikey']
    datatype = authenticate(apikey,device_id,sensor_id)
    if not datatype:
        return '请输入正确的apikey', 401
    if datatype['type']=='number':
        file_path = os.path.join(APP_DATA_DIR, sensor_id)
        try: text_list = open(file_path,'r').readlines()
        except IOError:
            return json.dumps({'sensor_id':sensor_id,'data':[]}), 404
        all_result = { # 获取到了数据
            'sensor_id':sensor_id,
            'data': list(map(lambda x: x.strip().split(','), text_list)), }
        return json.dumps(all_result), 200
    elif datatype['type']=='switch':
        file_path = os.path.join(APP_DATA_DIR, sensor_id)
        try: text_list = open(file_path,'r').readlines()
        except IOError:
            return json.dumps({'sensor_id':sensor_id,'data':[]}), 404
        all_result = { # 获取到了数据
            'sensor_id':sensor_id,
            'data': list(map(lambda x: x.strip().split(','), text_list)), }
        return json.dumps(all_result), 200
    elif datatype['type']=='gps':
        file_path = os.path.join(APP_DATA_DIR, sensor_id)
        try: text_list = open(file_path,'r').readlines()
        except IOError:return json.dumps({'sensor_id':sensor_id,'data':[]}),404
        data = []
        for text in text_list:
            a,b = re.match(r'([0-9-: ]*),([\s\S]*)\n',text).groups()
            data.append((a,json.loads(b)))
        all_result = {
            'sensor_id': sensor_id,
            'data': data,
            }
        return json.dumps(all_result), 200
    elif datatype['type']=='normal':
        file_path = os.path.join(APP_DATA_DIR, sensor_id)
        try: text_list = open(file_path, 'r').readlines()
        except IOError:return json.dumps({'sensor_id':sensor_id,'data':[]}),404
        data = []
        for text in text_list:
            a,b = re.match(r'([0-9-: ]*),([\s\S]*)\n',text).groups()
            data.append((a,json.loads(b)))
        all_result = {
            'sensor_id': sensor_id,
            'data': data,
            }
        return json.dumps(all_result), 200
    else:
        response = json.dumps({'reason':'此类数据暂时不支持查看'})
        return response, 401

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=23759,debug=True)
