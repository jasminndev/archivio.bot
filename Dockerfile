FROM python:3.13-alpine

WORKDIR bot/

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
