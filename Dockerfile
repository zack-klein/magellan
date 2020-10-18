FROM python:3.8-slim-buster

WORKDIR /root/webserver

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

RUN python setup.py develop
