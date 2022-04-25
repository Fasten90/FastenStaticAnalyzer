FROM ubuntu:22.04

RUN apt-get -y update

RUN apt-get -y install gcc

RUN apt-get -y install git

RUN apt-get -y install python3
RUN apt-get -y install python3-pip

COPY . .

RUN ./install.sh

CMD bash
