FROM ramwin/flask
MAINTAINER Xiang Wang "ramwi@163.com"
RUN apt-get install unzip
ADD gc-kafka-python-0.9.8.tar.gz /
ADD redis-2.10.5.tar.gz /
WORKDIR /redis-2.10.5
RUN python /redis-2.10.5/setup.py install
RUN python3 /redis-2.10.5/setup.py install
WORKDIR /gc-kafka-python-0.9.8
RUN python /gc-kafka-python-0.9.8/setup.py install
RUN python3 /gc-kafka-python-0.9.8/setup.py install
