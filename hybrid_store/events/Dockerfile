FROM python:3.8-slim-buster

WORKDIR /app

COPY events/ .
RUN pip3 install -r requirements.txt

CMD ["python", "kafka_events.py"]
