FROM python:latest

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt update \
    && apt install -y libpq-dev gcc

RUN pip install psycopg2

WORKDIR /code
COPY . /code/

# RUN adduser -D dockuser
# USER dockuser
# RUN chown dockuser:dockuser -R /code/