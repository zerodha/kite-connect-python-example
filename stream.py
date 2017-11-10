import sys
import json
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

import time
from db import insert_ticks
from kiteconnect import WebSocket

# Initialise.
kws = WebSocket("api_key", "public_token", "zerodha_user_id")

# RELIANCE BSE, RELIANCE NSE, NIFTY 50, SENSEX
tokens = [128083204, 73856, 256265, 265]


# Callback for tick reception.
def on_tick(ticks, ws):
	logging.info("on tick - {}".format(json.dumps(ticks)))
	insert_ticks.delay(ticks)


# Callback for successful connection.
def on_connect(ws):
	logging.info("Successfully connected to WebSocket")


def on_close():
	logging.info("WebSocket connection closed")


def on_error():
	logging.info("WebSocket connection thrown error")

# Assign the callbacks.
kws.on_tick = on_tick
kws.on_connect = on_connect
kws.on_close = on_close
kws.on_error = on_error

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
