FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN apt-get update \
 && apt-get upgrade -y \ 
 && apt-get dist-upgrade \
 && apt-get install openssl \
 && pip install --upgrade pip \
 && pip install -r /code/requirements.txt \
 && rm -rf ~/.cache

COPY . /code/

CMD ["python", "-m", "monitoringdaemon"]
