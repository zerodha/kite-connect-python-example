# Run celery workers
# celery -A db worker --loglevel=info

import sys
import json
import psycopg2
import logging
from celery import Celery
from datetime import datetime

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Configure with your own broker
app = Celery("tasks", broker="redis://localhost:6379/4")

# Initialize db
db = psycopg2.connect(database="ticks", user="postgres", password="password", host="127.0.0.1", port="5432")

# Db insert statement
insert_tick_statement = "INSERT INTO ticks (date, token, price) VALUES (%(date)s, %(token)s, %(price)s)"


# Task to insert to SQLite db
@app.task
def insert_ticks(ticks):
	c = db.cursor()
	for tick in ticks:
		c.execute(insert_tick_statement, {
			"date": datetime.now(),
			"token": tick["instrument_token"],
			"price": tick["last_price"]})

	logging.info("Inserting ticks to db : {}".format(json.dumps(ticks)))

	try:
		db.commit()
	except Exception:
		db.rollback()
		logging.exception("Couldn't write ticks to db: ")
