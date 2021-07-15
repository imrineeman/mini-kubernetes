# syntax=docker/dockerfile:1

FROM python:3.9-alpine

RUN apk update
RUN apk add python3-dev
RUN apk add --update docker openrc
RUN rc-update add docker boot
RUN pip3 install requests

EXPOSE 6000
WORKDIR /app
ARG CONTROLLER_IP
ARG CONTROLLER_PORT
ARG INTERVAL

ENV controller_ip = CONTROLLER_IP
ENV controller_port = CONTROLLER_PORT
ENV interval = INTERVAL

COPY . .

CMD python3 scheduler.py "$controller_ip" "$controller_port" "$interval"
