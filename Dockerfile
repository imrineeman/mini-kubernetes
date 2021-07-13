# syntax=docker/dockerfile:1

FROM python:3.9-alpine

RUN apk update
RUN apk add python3-dev
RUN apk add --update docker openrc
RUN rc-update add docker boot
RUN apk add docker-compose
RUN apk add py-pip
RUN apk add libffi-dev
RUN apk add openssl-dev
RUN apk add gcc
RUN apk add libc-dev
RUN apk add rust
RUN apk add cargo
RUN apk add make
RUN pip3 install docker-compose
    
EXPOSE 5000
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

ENTRYPOINT ["python3","-m","flask","run","--host=0.0.0.0"]