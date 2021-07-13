# syntax=docker/dockerfile:1

FROM python:3.9-alpine

RUN apk add python3
RUN apk add --update docker openrc
RUN rc-update add docker boot
RUN apk add docker-compose

EXPOSE 5000
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
