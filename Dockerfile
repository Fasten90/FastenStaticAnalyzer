FROM ubuntu:22.04

RUN apt-get -y update

RUN apt-get -y install gcc

CMD bash
