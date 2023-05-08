FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

WORKDIR /server

RUN apt-get update
RUN apt-get install -y gcc default-libmysqlclient-dev

RUN pip install pipenv
COPY requirements.txt /server/

RUN pip install -r requirements.txt

COPY . /server/

CMD uvicorn app.main:app --host "0.0.0.0" --port "8000" >> $LOG_FILE 2>&1
