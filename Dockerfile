FROM python:3.8.3-alpine3.11
MAINTAINER SaurabhT

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D saurabht
USER saurabht

