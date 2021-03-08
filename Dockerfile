FROM python:3.8

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src/