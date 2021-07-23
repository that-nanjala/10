FROM jupyter/scipy-notebook

WORKDIR /data

RUN pip install joblib

COPY train.csv ./train.csv


COPY train.py ./train.py
COPY inference.py ./inference.py

RUN python3 train.py


FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "streamlit", "run", "./scripts/dashboard.py", "--host=0.0.0.0"]