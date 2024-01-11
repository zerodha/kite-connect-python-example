import sys
import json
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

import time
from db import insert_ticks
from kiteconnect import KiteTicker

# Initialise.
kws = KiteTicker("your_api_key", "your_access_token")

# SBIN NSE, RELIANCE BSE, NIFTY 50, SENSEX
tokens = [779521, 128083204, 256265, 265]


# Callback for tick reception.
def on_ticks(ws, ticks):
	logging.info("on tick - {}".format(json.dumps(ticks)))
	insert_ticks.delay(ticks)


# Callback for successful connection.
def on_connect(ws, response):
	logging.info("Successfully connected to WebSocket")


def on_close(ws, code, reason):
	logging.info("WebSocket connection closed")


def on_error(ws, code, reason):
	logging.info("Connection error: {code} - {reason}".format(code=code, reason=reason))

# Callback when reconnect is on progress
def on_reconnect(ws, attempts_count):
    logging.info("Reconnecting: {}".format(attempts_count))

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close
kws.on_error = on_error
kws.on_reconnect = on_reconnect

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect(threaded=True)
# kws.connect(disable_ssl_verification=True) # for ubuntu

count = 0
while True:
	logging.info("This is main thread. Will subscribe to each token in tokens list with 5s delay")

	if count < len(tokens):
		if kws.is_connected():
			logging.info("Subscribing to: {}".format(tokens[count]))
			kws.subscribe([tokens[count]])
			kws.set_mode(kws.MODE_LTP, [tokens[count]])
			count += 1
		else:
			logging.info("Connecting to WebSocket...")

	time.sleep(5)
