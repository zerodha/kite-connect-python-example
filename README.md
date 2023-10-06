# Kite connect python client example

This is a simple example which uses [Python Kite connect client](https://github.com/rainmattertech/pykiteconnect) to receive ticks and save it to [Postgresql](https://www.postgresql.org/) database.
Celery is used as a Task queue manager to insert to database without blocking main Kite connect WebSocket thread.

Kite ticker subscribes to tokens in specified in `stream.py` with 5 second delay. Ticks received are sent to
celery taske queue where it will be inserted to db.

# Requirements

1. [Redis](https://redis.io) or any [AMQP client for Celery](http://docs.celeryproject.org/en/latest/getting-started/brokers/)
2. [Postgresql](https://www.postgresql.org/) db (Can be replaced with any other db)

# Install

```
pip install celery
pip install psycopg2
pip install kiteconnect
```

# Create database and table

Create a database called `ticks`

```
CREATE DATABASE ticks;
```

Create a table called `ticks` in `ticks` database

```
CREATE TABLE ticks (
    token integer NOT NULL,
    date timestamp without time zone,
    price double precision
);
```

# Configure celery and database in db.py

1. Update `broker` URL in `db.py` with redis or any other AMQP client.
2. Update `user`, `password` and `host` details for Postgresql in `db.py`

# Run Celery worker

```
celery -A db worker --loglevel=info
```

# Run Python client

```
python stream.py
```
