# syntax=docker/dockerfile:1

FROM python:3.9-alpine

RUN apk update
RUN apk add python3-dev
RUN apk add --update docker openrc
RUN rc-update add docker boot
RUN pip3 install requests

WORKDIR /app
ARG controller_ip
ARG controller_port
ARG interval

ENV CONTROLLER_IP = controller_ip
ENV CONTROLLER_PORT = controller_port
ENV INTERVAL = interval

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD python3 scheduler.py "$CONTROLLER_IP" "$CONTROLLER_PORT" "$INTERVAL"
