FROM python:3.10-slim

RUN mkdir /app

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD gunicorn --timeout=0 --workers=4 -b "0.0.0.0:5000" "run:create_app()"