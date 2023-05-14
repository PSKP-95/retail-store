FROM python:3.8.13-slim-bullseye

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT python -m uvicorn main:app --port 8001 --workers 4
